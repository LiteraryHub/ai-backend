import torch
import torch.nn as nn
import torchaudio

class Denoiser(nn.Module):
    """ Removes model bias from audio produced with hifigan """

    def __init__(self, hifigan, filter_length=1024, n_overlap=4,
                 win_length=1024, mode='zeros', **infer_kw):
        super().__init__()

        w = next(p for name, p in hifigan.named_parameters()
                 if name.endswith('.weight'))

        # self.stft = STFT(filter_length=filter_length,
        #                  hop_length=int(filter_length/n_overlap),
        #                  win_length=win_length).to(w.device)
        
        self.stft = torchaudio.transforms.Spectrogram(filter_length,
                          hop_length=int(filter_length/n_overlap),
                          win_length=win_length, power=None).to(w.device)
        self.istft = torchaudio.transforms.InverseSpectrogram(filter_length, 
                    hop_length=int(filter_length/n_overlap),
                    win_length=win_length).to(w.device)

        mel_init = {'zeros': torch.zeros, 'normal': torch.randn}[mode]
        mel_input = mel_init((1, 80, 88), dtype=w.dtype, device=w.device)

        with torch.no_grad():
            bias_audio = hifigan(mel_input, **infer_kw).float()

            if len(bias_audio.size()) > 2:
                bias_audio = bias_audio.squeeze(0)
            elif len(bias_audio.size()) < 2:
                bias_audio = bias_audio.unsqueeze(0)
            assert len(bias_audio.size()) == 2

            bias_spec = self.stft(bias_audio).abs()

        self.register_buffer('bias_spec', bias_spec[:, :, 0][:, :, None])

    def forward(self, audio, strength=0.1):
        audio_spec = self.stft(audio.float())
        audio_spec_mag, audio_spec_phase = audio_spec.abs(), audio_spec.angle()
        audio_spec_denoised = audio_spec_mag - self.bias_spec * strength
        audio_spec_denoised = torch.clamp(audio_spec_denoised, 0.0)
        audio_denoised = self.istft(audio_spec_denoised*torch.exp(1j*audio_spec_phase))
        return audio_denoised

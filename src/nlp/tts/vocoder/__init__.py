import torch
import json
from src.nlp.tts.vocoder.hifigan.env import AttrDict
from src.nlp.tts.vocoder.hifigan.models import Generator

def load_hifigan(state_dict_path, config_file):
    with open(config_file) as f:
        data = f.read()
    json_config = json.loads(data)
    h = AttrDict(json_config)

    generator = Generator(h)    
    state_dict_g = torch.load(state_dict_path, map_location='cpu')
    generator.load_state_dict(state_dict_g['generator'])

    generator.eval()
    generator.remove_weight_norm()
    return generator

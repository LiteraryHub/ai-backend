from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from warnings import simplefilter
from src.api.restricted_topic_detection.endpoints import router as restricted_topic_detection_router
from src.api.audiobook_generator.endpoints import router as audiobook_generator_router
from src.api.extract_text.endpoints import router as text_extractor_router
from src.api.book_cover_generator.endpoints import router as book_cover_generator_router
from src.api.author_pipeline.endpoints import router as author_pipeline_router
from pyngrok import ngrok
import nest_asyncio
import warnings

# Setup function for ngrok
def start_ngrok():
    authtoken = "2Ue97ZgIffXxclCCYhsjDdFYjK9_4LE6HHTdrXZttvE2MJQ9Z"
    ngrok.set_auth_token(authtoken)
    tunnel = ngrok.connect(8000)
    print('Public URL:', tunnel.public_url)
    nest_asyncio.apply()

# Ignore PyTorch UserWarnings
warnings.filterwarnings("ignore", category=UserWarning, module="torch")
warnings.filterwarnings("ignore", category=FutureWarning, module="torch")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="torch")
warnings.filterwarnings("ignore", category=UserWarning, module="transformers")
warnings.filterwarnings("ignore", category=FutureWarning, module="transformers")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="transformers")
simplefilter(action='ignore', category=FutureWarning)

# Create a new FastAPI app
app = FastAPI(
    title='LiteraryHub API',
    contact={'email': 'moemen.ayman@aiu.edu.eg'},
    license={
        'name': 'Apache 2.0',
        'url': 'http://www.apache.org/licenses/LICENSE-2.0.html',
    },
    version='1.0.11',
    servers=[{'url': 'http://localhost:8000', 'description': 'Local server'}],
)

# Allow all origins to access the API (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers in the main app
app.include_router(audiobook_generator_router, prefix='/audiobook', tags=['Audiobook Generator'])
app.include_router(text_extractor_router, prefix='/extractor', tags=['Text Extractor'])
app.include_router(book_cover_generator_router, prefix='/book-cover', tags=['Book Cover Generator'])
app.include_router(restricted_topic_detection_router, prefix='/restricted-topic-detection', tags=['Restricted Topic Detection'])
app.include_router(author_pipeline_router, prefix='/pipeline', tags=['Author Pipeline'])


@app.on_event("startup")
async def startup_event():
    start_ngrok()
    
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
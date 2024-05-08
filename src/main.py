from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
# from src.api.book_cover_generator.endpoints import router as book_cover_generator_router
from src.api.audiobook_generator.endpoints import router as audiobook_generator_router
from src.api.extract_text.endpoints import router as text_extractor_router
from src.api.book_cover_generator.endpoints import router as book_cover_generator_router
from src.api.author_pipeline.endpoints import router as author_pipeline_router
import warnings

# Ignore PyTorch UserWarnings
warnings.filterwarnings("ignore", category=UserWarning, module="torch")

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
# app.include_router(book_cover_generator_router, prefix='/book-cover-generator', tags=['Book Cover Generator'])
app.include_router(audiobook_generator_router, prefix='/audiobook', tags=['Audiobook Generator'])
app.include_router(text_extractor_router, prefix='/extractor', tags=['Text Extractor'])
app.include_router(book_cover_generator_router, prefix='/book-cover', tags=['Book Cover Generator'])
app.include_router(author_pipeline_router, prefix='/pipeline', tags=['Author Pipeline'])


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
import os

from concurrent.futures import ThreadPoolExecutor

from langchain_openai import ChatOpenAI

from agentic_profile_matching.adapters.embedding_generator.openai_embedding_generator import OpenAIEmbeddingGenerator
from agentic_profile_matching.adapters.vector_store.pg_vector_store import PGVectorStore
from agentic_profile_matching.app.pipeline.pipeline import Pipeline
from agentic_profile_matching.app.pipeline.steps.chunking_step import ChunkingStep
from agentic_profile_matching.app.pipeline.steps.embedding_generation_step import EmbeddingGenStep
from agentic_profile_matching.app.pipeline.steps.extract_data_step import ExtractDataStep
from agentic_profile_matching.app.pipeline.steps.metatadata_extraction_step import MetadataExtractionStep
from agentic_profile_matching.app.pipeline.steps.save_vectors_step import SaveVectorStep
from agentic_profile_matching.app.utils import bootstrap
from agentic_profile_matching.app.utils.container import Container
from agentic_profile_matching.configs import register_singletons
from agentic_profile_matching.configs.constants import Constants
from agentic_profile_matching.configs.logging.logging_config import APMLogger

def build_ingestion_pipeline():
    llm = Container.resolve(ChatOpenAI)

    ingestion_pipeline = (
        Pipeline
            .start(ExtractDataStep())
            .pipe(MetadataExtractionStep(llm))
            .pipe(ChunkingStep())
            .pipe(EmbeddingGenStep(OpenAIEmbeddingGenerator()))
            .pipe(SaveVectorStep(PGVectorStore()))
    )

    return ingestion_pipeline

def process_file(filepath: str):
    try:
        ingestion_pipeline = build_ingestion_pipeline()

        print(f"Processing file: {filepath}")
        ingestion_pipeline.run(filepath)

    except Exception as e:
        print(f"[ERROR] {filepath}: {e}")
        raise

def iter_files(root_dir: str):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            yield os.path.join(dirpath, filename)

@bootstrap([
    APMLogger.init,
    register_singletons
])
def main():
    resumes_dir_path = os.path.join(os.getcwd(), Constants.RESUMES_DIR_PATH)

    print("Ingesting...")

    with ThreadPoolExecutor(max_workers=Constants.INGESTION_MAX_WORKERS) as executor:
        for filepath in iter_files(resumes_dir_path):
            executor.submit(process_file, filepath)

    print("Ingesting Completed.")
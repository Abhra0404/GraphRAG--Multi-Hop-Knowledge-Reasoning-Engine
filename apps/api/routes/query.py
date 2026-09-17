import logging

from fastapi import APIRouter, HTTPException

from apps.api.schemas.query import QueryRequest, QueryResponse
from reasoning.pipeline import answer_query


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/query",
    tags=["query"],
)


@router.post(
    "",
    response_model=QueryResponse,
    summary="Answer a knowledge query",
    description=(
        "Retrieves relevant document evidence and knowledge "
        "graph paths, performs multi-hop reasoning, and "
        "generates a cited answer."
    ),
)
def query(request: QueryRequest) -> QueryResponse:
    logger.info("Processing query: %s", request.question)

    try:
        result = answer_query(request.question)

        logger.info("Query completed successfully")

        return QueryResponse(
            answer=result["answer"],
            entities=result["entities"],
            evidence=result["evidence"],
        )

    except ValueError as exc:
        logger.warning("Query validation error: %s", exc)

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception:
        logger.exception("Unexpected error while processing query")

        raise HTTPException(
            status_code=500,
            detail="Internal server error.",
        )
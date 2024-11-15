import asyncio
from typing import get_args, get_origin, get_type_hints

from fastapi import FastAPI
from fastapi.routing import APIRoute
from jax.apiutils import CollectionResponse, StreamingResponse, Response


def get_return_type(route: APIRoute) -> type:
    """Extract the return type from a FastAPI route's response model."""
    # Get the original function (beneath FastAPI decorators)
    original_func = route.endpoint

    # Get type hints for the function
    type_hints = get_type_hints(original_func)

    # FastAPI functions should have a return type annotation
    if "return" not in type_hints:
        raise ValueError(f"Route {route.path} is missing return type annotation")

    return type_hints["return"]


def is_valid_return_type(typ: type) -> bool:
    """Check if a type is either Response, CollectionResponse, or an Optional/Union containing them.
    Also handles async return types.
    """
    # Handle Optional/Union types
    origin = get_origin(typ)
    if origin is not None:
        # If it's a Union/Optional, check all possible types
        if origin in (Union, types.UnionType):  # type: ignore
            return any(is_valid_return_type(arg) for arg in get_args(typ))
        # Handle async return types
        if asyncio.iscoroutinefunction(origin):
            # For async functions, check the actual return type (last type arg)
            args = get_args(typ)
            if args:
                return is_valid_return_type(args[-1])

    # Check if type is Response or CollectionResponse
    return any(
        issubclass(typ, expected_type)
        for expected_type in (Response, CollectionResponse, StreamingResponse)
    )


def test_get_endpoint_return_types(app: FastAPI):
    """Test that all GET endpoints return either Response or CollectionResponse.

    Args:
    ----
        app: Your FastAPI application instance

    """
    invalid_routes = []

    for route in app.routes:
        if not isinstance(route, APIRoute) or route.methods != {"GET"}:
            continue

        try:
            return_type = get_return_type(route)
            if not is_valid_return_type(return_type):
                invalid_routes.append(
                    f"GET Route {route.path} ({route.name}) returns {return_type}"
                    "which is not a Response or CollectionResponse"
                )
        except ValueError as e:
            invalid_routes.append(str(e))

    assert not invalid_routes, "\n".join(invalid_routes)

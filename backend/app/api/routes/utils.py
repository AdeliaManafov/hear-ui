from fastapi import APIRouter
from fastapi import Request
import logging

from app.core.model_wrapper import ModelWrapper

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/utils", tags=["utils"])


# The test-email endpoint has been removed for the MVP. Keep health_check only.


@router.get("/health-check/")
async def health_check():
    """Return a small JSON status object for health checks."""
    return {"status": "ok"}


@router.get("/model-info/")
async def model_info(request: Request):
    """Return information about the loaded model (for debug only).

    This endpoint is intended for local development and debugging to quickly
    verify whether the model was loaded at startup and what shape it expects.
    """
    wrapper: ModelWrapper | None = getattr(request.app.state, "model_wrapper", None)
    if wrapper is None:
        return {"loaded": False, "reason": "no model wrapper attached to app.state"}

    info: dict = {"loaded": wrapper.is_loaded()}
    if wrapper.is_loaded():
        m = wrapper.model
        info["model_type"] = repr(type(m))
        # expose feature names if available (sklearn stores feature_names_in_)
        try:
            fnames = getattr(m, "feature_names_in_", None)
            if fnames is not None:
                info["feature_names_in_"] = list(map(str, fnames))
        except Exception:
            pass
        # Try to expose n_features_in_ (sklearn) or length of coef_
        n_features = getattr(m, "n_features_in_", None)
        if n_features is None:
            coef = getattr(m, "coef_", None)
            try:
                if coef is not None:
                    import numpy as _np

                    coef_arr = _np.array(coef)
                    # if 2D, take last axis
                    if coef_arr.ndim > 1:
                        n_features = int(coef_arr.shape[-1])
                    else:
                        n_features = int(coef_arr.shape[0])
            except Exception:
                n_features = None
        info["expected_n_features"] = n_features
    else:
        # include possible path for diagnostics
        try:
            info["model_path"] = str(request.app.state.model_wrapper.model_path)
        except Exception:
            pass
    logger.debug("model-info: %s", info)
    return info

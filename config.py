from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi import Request

router = InferringRouter()

@cbv(router)
class FastApi:
    router      = router
    request     = Request

    def HttpResponse(
        response:dict,
        code:int=1,
        comment:str="ok"
    ):return {
        "meta":{
            "code":code,
            "comment":comment
        },
        "data":response
    }
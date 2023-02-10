import json
from datetime import datetime
from todoApp.interface import Todo
from uuid import uuid4

'''
class Controller todo
'''
class CTodo(Todo):
    
    '''
    @POST
    /todo
    application/json
    {
        "title":"Konten Judul",
        "description":"Konten Deskripsi"
    }
    '''
    @Todo.router.post("/todo")
    async def create(item: Todo.request):
        item_verify = await Todo.Verify.create(item)
        Todo.todo_list.append({
            "id":uuid4().hex,
            **json.loads(item_verify.json())
        })
        return Todo.HttpResponse({
            "success":True
        })


    '''
    @GET
    /todo
    '''
    @Todo.router.get("/todo")
    async def data():
        return Todo.HttpResponse(Todo.todo_list)


    '''
    @GET
    /todo/{id}
    '''
    @Todo.router.get("/todo/{id}")
    async def dataById(id:str):
        data = list(filter(lambda x: x["id"] == id, Todo.todo_list))
        if len(data) == 0: return Todo.HttpResponse(None)
        return Todo.HttpResponse(data[0])


    '''
    @PUT
    /todo/{id}
    application/json
    {
        "title":"Konten Judul", << tidak wajib
        "description":"Konten Deskripsi" << tidak wajib
    }
    '''
    @Todo.router.put("/todo/{id}")
    async def update(item:Todo.request,id:str):
        item_verify = await Todo.Verify.update(id,item)
        error_catch = None
        for m in Todo.todo_list:
            if m["id"] == id:
                try:
                    if m["delete_at"] != None: raise Exception("Todo already deleted")
                    if m["finished_at"] != None: raise Exception("Todo already finished")
                    m.update(item_verify)
                except Exception as E:
                    error_catch = f"{E}"
        if error_catch: return Todo.HttpResponse(None,code=2,comment=error_catch)
        return Todo.HttpResponse({
            "success":True
        })


    '''
    @DELETE
    /todo/{id}
    '''
    @Todo.router.delete("/todo/{id}")
    async def delete(id:str):
        error_catch = None
        for m in Todo.todo_list:
            if m["id"] == id:
                try:
                    if m["delete_at"] != None: raise Exception("Todo already deleted")
                    m.update({"delete_at":datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                except Exception as E:
                    error_catch = f"{E}"
        if error_catch: return Todo.HttpResponse(None,code=2,comment=error_catch)
        return Todo.HttpResponse({
            "success":True
        })


    '''
    @PATCH
    /todo/{id}/finish
    '''
    @Todo.router.patch("/todo/{id}/finish")
    async def close(id:str):
        error_catch = None
        for m in Todo.todo_list:
            if m["id"] == id:
                try:
                    if m["delete_at"] != None: raise Exception("Todo already deleted")
                    if m["finished_at"] != None: raise Exception("Todo already finished")
                    m.update({"finished_at":datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                except Exception as E:
                    error_catch = f"{E}"
        if error_catch: return Todo.HttpResponse(None,code=2,comment=error_catch)
        return Todo.HttpResponse({
            "success":True
        })

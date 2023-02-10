import json
from datetime import datetime
from todoApp.config import FastApi
from pydantic import BaseModel
from typing import Optional

class Todo(FastApi):

    '''
    karena tidak menggunakan database
    jadi pada contoh ini akan menggunakan
    In Memory Allocation, dikarenakan
    tidak adanya login, Maka memory allocation
    dibawah ini bebas digunakan session siapa saja.
    '''
    todo_list:list=[]
    

    '''
    Class ini untuk mendefinisikan 
    payload todo yang akan masuk
    '''
    class Create(BaseModel):
        title : str 
        description : str 
        finished_at : Optional[str] = None
        created_at : Optional[str] = None
        updated_at : Optional[str] = None
        delete_at : Optional[str] = None

    class Update(BaseModel):
        title : Optional[str] = None
        description : Optional[str] = None

    '''
    Mendapatkan value default atau value awal
    dari sebuah todo, jika sudah terupdate
    makan akan mengambil value terbaru
    '''
    def default(id):
        return list(filter(lambda x: x["id"] == id, Todo.todo_list))
        
    '''
    Jika ingin mengimplementasikan 
    data integrity
    '''
    class Verify:
        async def create(payload):
            item = await payload.json()
            verify = Todo.Create(**{
                "created_at":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                **item
            })
            return verify

        async def update(id,payload):
            item     = await payload.json()
            verify   = json.loads(Todo.Update(**item).json())
            default  = Todo.default(id)
            if len(default) == 0: return None
            default  = default[0]
            verify = {
                **Todo.default(id),
                **{
                    "title"       :default['title']       if verify['title']       == None else verify['title'],
                    "description" :default['description'] if verify['description'] == None else verify['description'],
                    "updated_at"  :datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            }
            return verify
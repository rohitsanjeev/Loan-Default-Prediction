# from fastapi import FastAPI
# #run in virtual env
# #python --m venv venv(name of the env)
# #to activate the env 
# # pip install fastapi uvicorn
# #venv\Scripts\activate (windows)
# #to run the app
# ##uvicorn main:app --reload (reload --> to auto update the changes in the code)

# app = FastAPI() ##---> instance

# @app.get("/") ##'/' ---> root point
# def read_root(): # function
#     #here comes business 
#     return {"theycallhimog(2025)"}

# #sub url creation
# @app.get("/sub")
# def internal_url():
#     return {"meassage": "this is the internal url page"}

# #####-----> PATH PARAMETERS <-----
# #DEF--> a path parameter is a variable part of a url path, 
# # used to identify a specific resource

# @app.get()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from math import pow

app = FastAPI(title="Calculator API", description="A simple calculator API with multiple operations", version="1.0.0")


# -----------------------------
# Pydantic Models
# -----------------------------
class Numbers(BaseModel):
    a: float = Field(..., description="First number")
    b: float = Field(..., description="Second number")


class Result(BaseModel):
    operation: str
    a: float
    b: float
    result: float


class ErrorResponse(BaseModel):
    error: str


# In-memory history
history: List[Result] = []


# -----------------------------
# Utility functions
# -----------------------------
def save_history(op: str, a: float, b: float, result: float):
    """Save operation result to in-memory history"""
    history.append(Result(operation=op, a=a, b=b, result=result))


# -----------------------------
# API Endpoints
# -----------------------------
@app.get("/", summary="Home endpoint")
def home():
    """
    Welcome message for the calculator API
    """
    return {"message": "Welcome to the FastAPI Calculator!"}


@app.get("/history", response_model=List[Result], summary="Get operation history")
def get_history():
    """
    Returns a list of all previous calculations
    """
    return history


@app.post("/add", response_model=Result, summary="Add two numbers")
def add(nums: Numbers):
    """
    Add two numbers and return the result
    """
    result = nums.a + nums.b
    save_history("add", nums.a, nums.b, result)
    return Result(operation="add", a=nums.a, b=nums.b, result=result)


@app.post("/subtract", response_model=Result, summary="Subtract two numbers")
def subtract(nums: Numbers):
    """
    Subtract b from a and return the result
    """
    result = nums.a - nums.b
    save_history("subtract", nums.a, nums.b, result)
    return Result(operation="subtract", a=nums.a, b=nums.b, result=result)


@app.post("/multiply", response_model=Result, summary="Multiply two numbers")
def multiply(nums: Numbers):
    """
    Multiply two numbers and return the result
    """
    result = nums.a * nums.b
    save_history("multiply", nums.a, nums.b, result)
    return Result(operation="multiply", a=nums.a, b=nums.b, result=result)


@app.post("/divide", response_model=Result, responses={400: {"model": ErrorResponse}}, summary="Divide two numbers")
def divide(nums: Numbers):
    """
    Divide a by b. Returns error if b is zero.
    """
    if nums.b == 0:
        raise HTTPException(status_code=400, detail="Cannot divide by zero!")
    result = nums.a / nums.b
    save_history("divide", nums.a, nums.b, result)
    return Result(operation="divide", a=nums.a, b=nums.b, result=result)


@app.post("/power", response_model=Result, summary="Power operation")
def power(nums: Numbers):
    """
    Raise a to the power of b
    """
    result = pow(nums.a, nums.b)
    save_history("power", nums.a, nums.b, result)
    return Result(operation="power", a=nums.a, b=nums.b, result=result)


@app.post("/modulus", response_model=Result, responses={400: {"model": ErrorResponse}}, summary="Modulus operation")
def modulus(nums: Numbers):
    """
    Returns a % b. Raises error if b is zero.
    """
    if nums.b == 0:
        raise HTTPException(status_code=400, detail="Cannot modulo by zero!")
    result = nums.a % nums.b
    save_history("modulus", nums.a, nums.b, result)
    return Result(operation="modulus", a=nums.a, b=nums.b, result=result)


@app.post("/floor_divide", response_model=Result, responses={400: {"model": ErrorResponse}}, summary="Floor division")
def floor_divide(nums: Numbers):
    """
    Returns floor division a // b. Raises error if b is zero.
    """
    if nums.b == 0:
        raise HTTPException(status_code=400, detail="Cannot divide by zero!")
    result = nums.a // nums.b
    save_history("floor_divide", nums.a, nums.b, result)
    return Result(operation="floor_divide", a=nums.a, b=nums.b, result=result)

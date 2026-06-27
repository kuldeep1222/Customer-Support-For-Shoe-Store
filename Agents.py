## Agent.py



## plain with LLM

import os
import json
from dotenv import load_dotenv

from openai import OpenAI
from Tools import get_order,get_product,search_products,compare_products,recommend_products,find_alternatives


load_dotenv()

mykey = os.getenv("GEMINI_API_KEY")

gemini_base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"

client = OpenAI(api_key=mykey, base_url=gemini_base_url)

SYSTEM_PROMPT = """
You are an AI Planning Agent for an online shoe store.

Your ONLY responsibility is to decide which tool(s) should be executed.

DO NOT answer the customer.
DO NOT explain your reasoning.
DO NOT invent tools or intents.
Return ONLY valid JSON.

========================
AVAILABLE TOOLS
========================

1. get_order

Purpose:
Retrieve order details.

Arguments:
{
    "order_id": "ORD-1002"
}

--------------------------------------------------------

2. get_product

Purpose:
Retrieve product details.

Arguments:
{
    "product_id": "P001"
}

--------------------------------------------------------

3. search_products

Purpose:
Search products based on filters.

Arguments:
{
    "brand": null,
    "category": null,
    "name": null,
    "max_price": null,
    "min_price": null,
    "size": null,
    "in_stock": null
}

Only include fields explicitly mentioned by the user.

--------------------------------------------------------

4. compare_products

Purpose:
Compare TWO SPECIFIC PRODUCTS.

Use ONLY when the user explicitly asks to compare two products.

Arguments:
{
    "product1_id": "",
    "product2_id": ""
}

DO NOT use this tool for brand comparison or searching alternatives.

--------------------------------------------------------

5. recommend_products

Purpose:
Recommend products matching user preferences.

Arguments:
{
    "category": null,
    "brand": null,
    "max_price": null
}

--------------------------------------------------------

6. find_alternatives

Purpose:
Find cheaper or similar alternatives for ONE product.

Arguments:
{
    "product_id": ""
}

If product_id comes from a previous tool, use

"$previous.product_id"

If size comes from a previous tool, use

"$previous.size"

Example:

{
    "tool":"get_order",
    "arguments":{
        "order_id":"ORD-1002"
    }
},
{
    "tool":"find_alternatives",
    "arguments":{
        "product_id":"$previous.product_id"
    }
}

========================
TOOL SELECTION RULES
========================

Rule 1:
For order tracking,
ALWAYS use get_order().

Rule 2:
For product details,
ALWAYS use get_product().

Rule 3:
For searching products,
ALWAYS use search_products().

Rule 4:
If the user asks for a cheaper or similar alternative to an ordered product,

ALWAYS use

get_order()

THEN

find_alternatives()

Rule 5:
If the user asks to compare two specific products,

ALWAYS use compare_products().

Rule 6:
If the user compares BRANDS instead of products,
FIRST search both brands using search_products().
Do NOT call compare_products() because it only compares two specific products.

Rule 7:
If multiple tools are required,
return them in execution order.

========================
ALLOWED INTENTS
========================

track_order

product_details

search_products

compare_products

recommend_products

find_alternatives

Never invent any other intent.

========================
OUTPUT FORMAT
========================

Return ONLY JSON.

Example 1

{
    "intent":"track_order",
    "tools":[
        {
            "tool":"get_order",
            "arguments":{
                "order_id":"ORD-1002"
            }
        }
    ]
}

Example 2

{
    "intent":"find_alternatives",
    "tools":[
        {
            "tool":"get_order",
            "arguments":{
                "order_id":"ORD-1002"
            }
        },
        {
            "tool":"find_alternatives",
            "arguments":{
                "product_id":"$previous.product_id"
            }
        }
    ]
}

Example 3

{
    "intent":"compare_products",
    "tools":[
        {
            "tool":"compare_products",
            "arguments":{
                "product1_id":"P001",
                "product2_id":"P009"
            }
        }
    ]
}
Example 4
{
    "user":"Nike shoes",

    "output":{

        "intent":"search_products",

        "tools":[
            {
                "tool":"search_products",
                "arguments":{
                    "brand":"Nike"
                }
            }
        ]
    }
}
Example 5
{
    "user":"Adidas running shoes under 5000",

    "output":{

        "intent":"search_products",

        "tools":[
            {
                "tool":"search_products",
                "arguments":{
                    "brand":"Adidas",
                    "category":"running shoes",
                    "max_price":5000
                }
            }
        ]
    }
}
Example 6
{
    "user":"Recommend Nike casual shoes",

    "output":{

        "intent":"recommend_products",

        "tools":[
            {
                "tool":"recommend_products",
                "arguments":{
                    "brand":"Nike",
                    "category":"casual shoes"
                }
            }
        ]
    }
}
Example 7
{
    "user":"Tell me about product P001",

    "output":{

        "intent":"product_details",

        "tools":[
            {
                "tool":"get_product",
                "arguments":{
                    "product_id":"P001"
                }
            }
        ]
    }
}
Example 8 
{User:
Show Nike and Puma shoes under ₹5000

    Output:

    {
    "intent":"search_products",
    "tools":[
        {
        "tool":"search_products",
        "arguments":{
            "brand":"Nike",
            "max_price":5000
        }
        },
        {
        "tool":"search_products",
        "arguments":{
            "brand":"Puma",
            "max_price":5000
        }
        }
    ]
    }
}
Also think beyond this example dont learn this limited example 
Classify the user's request using semantic meaning.

Examples:

- "Nike shoes" → search_products
- "Adidas running shoes" → search_products
- "Recommend Puma shoes" → recommend_products
- "Tell me about P001" → product_details
- "Track order ORD-1002" → track_order
"""
 
def plan_with_llm(question):
    try:

        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question}
            ],
            response_format={"type": "json_object"}, # Force JSON response
            temperature=0
        )

        content = response.choices[0].message.content

        # Convert JSON string to Python dictionary
        plan = json.loads(content)

        return plan

    except json.JSONDecodeError:
        return {
            "error": "Invalid JSON returned by LLM."
        }

    except Exception as e:
        return {
            "error": f"LLM Error: {str(e)}"
        }
    
### VALIDATOR  --> check llm's plan valid or not


ALLOWED_INTENTS = {
    "track_order",
    "product_details",
    "search_products",
    "compare_products",
    "recommend_products",
    "find_alternatives"
}

ALLOWED_TOOLS = {
    "get_order": ["order_id"],
    "get_product": ["product_id"],
    "search_products": [],
    "compare_products": ["product1_id", "product2_id"],
    "recommend_products": [],
    "find_alternatives": ["product_id"]
}


def validate_plan(plan):
    """
    Validate the execution plan returned by the LLM.

    Returns:
        (True, None) if valid

        (False, "Reason") if invalid
    """

 
    # Plan must be a dictionary
   
    if not isinstance(plan, dict):
        return False, "Plan must be a dictionary."

    # Intent check

    intent = plan.get("intent")

    if not intent:
        return False, "Missing intent."

    if intent not in ALLOWED_INTENTS:
        return False, f"Invalid intent: {intent}"

  
    # Tools check
  
    tools = plan.get("tools")

    if not isinstance(tools, list):
        return False, "Tools must be a list."

    if len(tools) == 0:
        return False, "No tools provided."


    # Validate each tool

    for step in tools:

        if not isinstance(step, dict):
            return False, "Each tool must be an object."

        tool_name = step.get("tool")

        if tool_name not in ALLOWED_TOOLS:
            return False, f"Unknown tool: {tool_name}"

        arguments = step.get("arguments", {})

        if not isinstance(arguments, dict):
            return False, f"Arguments for {tool_name} must be a dictionary."

        required_args = ALLOWED_TOOLS[tool_name]

        for arg in required_args:

            if arg not in arguments:
                return False, f"Missing '{arg}' for tool '{tool_name}'."

            value = arguments[arg]

            if value in ("", None):
                return False, f"'{arg}' cannot be empty."
                
        for value in arguments.values():

            if isinstance(value, str) and value.startswith("previous."):

                if tool_name == "get_order":
                    return False, "First tool cannot use previous placeholders."

    return True, None



## Execute the valid plan

def execute_plan(plan):
    """
    Executes the validated execution plan.
    """

    results = []
    previous_output = None

    tool_map = {
        "get_order": get_order,
        "get_product": get_product,
        "search_products": search_products,
        "compare_products": compare_products,
        "recommend_products": recommend_products,
        "find_alternatives": find_alternatives
    }

    try:

        for step in plan["tools"]:

            tool_name = step["tool"]

            arguments = step.get("arguments", {}).copy()

         
            # Resolve placeholders
           

            if previous_output:

                for key, value in arguments.items():

                    if isinstance(value, str) and value.startswith("$previous."):

                        field = value.replace("$previous.", "")

                        if field in previous_output:

                            arguments[key] = previous_output[field]

                        else:

                            return {
                                "success": False,
                                "error": f"'{field}' not found in previous tool output."
                            }

            tool = tool_map.get(tool_name)

            if tool is None:

                return {
                    "success": False,
                    "error": f"Unknown tool '{tool_name}'."
                }

            output = tool(**arguments)

            if isinstance(output, dict) and output.get("success") is False:
                return output

            results.append({
                "tool": tool_name,
                "arguments": arguments,
                "output": output
            })

            previous_output = output

        return {
            "success": True,
            "results": results
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }
    


## Formats the response generated by llm

def format_response(execution):

    if not execution["success"]:
        return f" {execution['error']}"

    tool = execution["results"][-1]["tool"]
    data = execution["results"][-1]["output"]

    # Product Details


    if tool == "get_product":

        return (
            f"   {data['name']}\n\n"
            f" Brand: {data['brand']}\n"
            f" Category: {data['category']}\n"
            f" Price: ₹{data['price']}\n"
            f" Sizes: {', '.join(map(str, data['sizes_available']))}\n"
            f" Stock: {data['pieces_available']} pairs\n"
            f" {data['description']}"
        )


    # Order Details


    elif tool == "get_order":

        return (
            f" Order ID: {data['order_id']}\n\n"
            f" Product ID: {data['product_id']}\n"
            f" Status: {data['status']}\n"
            f" Ordered On: {data['ordered_on']}\n"
            f" Expected Delivery: {data['expected_delivery']}\n"
            f" Quantity: {data['quantity']}"
        )


    # Search Products / Recommendations / Alternatives


    elif tool in ["search_products", "recommend_products", "find_alternatives"]:

        if len(data) == 0:
            return " No matching products found."

        text = " **Matching Products**\n\n"

        for p in data:

            text += (
                f"•    {p['name']}\n"
                f"   Brand: {p['brand']}\n"
                f"   Price: ₹{p['price']}\n"
                f"   Sizes: {', '.join(map(str, p['sizes_available']))}\n"
                f"   Stock: {p['pieces_available']} pairs\n\n"
            )

        return text

    # ----------------------------------
    # Compare Products
    # ----------------------------------

    elif tool == "compare_products":

        p1 = data["product_1"]
        p2 = data["product_2"]

        return (
            f"   Product Comparison\n\n"
            f" {p1['name']}\n"
            f"Brand: {p1['brand']}\n"
            f"Price: ₹{p1['price']}\n\n"
            f"VS\n\n"
            f" {p2['name']}\n"
            f"Brand: {p2['brand']}\n"
            f"Price: ₹{p2['price']}\n\n"
            f" Cheaper Product: {data['cheaper_product']}\n"
            f"₹ Price Difference: {data['price_difference']}"
        )


    return str(data)

# final 



def run_agent(question):

  
    # Planning
 

    plan = plan_with_llm(question)

    if isinstance(plan, dict) and "error" in plan:
     
        return plan["error"]

    

    # Validation


    valid, error = validate_plan(plan)

    if not valid:

        

        if "Missing" in error or "cannot be empty" in error:

            return (
                " Missing information.\n\n"
                f"{error}\n\n"
                "Please provide the required information and try again."
            )

        return f" Invalid execution plan.\n\n{error}"


    # Execute
 

    execution = execute_plan(plan)

    

 
    # Format Response

    response = format_response(execution)

   

    return response
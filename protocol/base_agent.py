from typing import Callable


class BaseAgent:
    def __init__(self, tool_layer: Callable):
        self.tool_layer = tool_layer
        self.methods = self.get_supported_methods()

    def get_supported_methods(self) -> dict:
        """
        Returns a map of JSON-RPC method names to handler methods.
        Should be overridden by child classes.
        """
        raise NotImplementedError("Agents must define supported methods.")

    async def handle_rpc(self, request: dict) -> dict:
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")

        if method not in self.methods:
            return {
                "jsonrpc": "2.0",
                "error": {"code": -32601, "message": f"Method '{method}' not found"},
                "id": request_id,
            }

        try:
            result = self.methods[method](params)
            return {"jsonrpc": "2.0", "result": result, "id": request_id}
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "error": {"code": -32000, "message": str(e)},
                "id": request_id,
            }

import grpc
import cart_pb2
import cart_pb2_grpc

channel = grpc.insecure_channel("grpc-cart-service:50051")
stub = cart_pb2_grpc.CartServiceStub(channel)

def get_cart_by_id(id: str, fields: list[str]):
    request = cart_pb2.GetCartRequest(id=id, fields=fields)

    response = stub.GetCart(request)
    return response.cart

def create_cart(id: str, product_id: str, quantity: int) -> str:
    request = cart_pb2.CreateCartRequest(
        id=id,
        product_id=product_id,
        quantity=quantity
    )

    response = stub.CreateCart(request)
    return response.message

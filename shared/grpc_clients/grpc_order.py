import grpc
import order_pb2
import order_pb2_grpc

channel = grpc.insecure_channel("grpc-order-service:50053")
stub = order_pb2_grpc.OrderServiceStub(channel)

def place_order(id: str, item_id: str, quantity: int) -> str:
    response = stub.PlaceOrder(order_pb2.OrderRequest(
        id=id,
        item_id=item_id,
        quantity=quantity
    ))

    return response.message

def refund_order(id: str) -> str:
    response = stub.RefundOrder(order_pb2.RefundRequest(id=id))

    return response.message

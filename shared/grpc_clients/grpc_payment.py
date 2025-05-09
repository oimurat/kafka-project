import grpc
import payment_pb2
import payment_pb2_grpc

channel = grpc.insecure_channel("grpc-payment-service:50054")
stub = payment_pb2_grpc.PaymentServiceStub(channel)

def pay_order(order_id: str, amount: int) -> str:
    response = stub.PayOrder(payment_pb2.PaymentRequest(order_id=order_id, amount=amount))

    return response.message

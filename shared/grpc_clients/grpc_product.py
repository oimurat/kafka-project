import grpc
import product_pb2
import product_pb2_grpc

channel = grpc.insecure_channel("grpc-product-service:50052")
stub = product_pb2_grpc.ProductServiceStub(channel)

def get_product_by_id(product_id: str, fields: list[str]):
    request = product_pb2.GetProductRequest(id=product_id, fields=fields)
    response = stub.GetProduct(request)

    return response.product

def update_product(id: str, name: str, price: float, description: str):
    request = product_pb2.UpdateProductRequest(
        id=id,
        name=name,
        price=price,
        description=description
    )
    
    response = stub.UpdateProduct(request)

    return response.product

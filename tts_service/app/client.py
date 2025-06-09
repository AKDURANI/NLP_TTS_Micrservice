import grpc
import sys
import os

# Add the grpc_gen directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'grpc_gen')))

# Import the generated gRPC code
import tts_pb2
import tts_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = tts_pb2_grpc.TextToSpeechStub(channel)
        request = tts_pb2.GenerateRequest(
            pdf_path="C:/NLP_Project/RichDadPoorDad.pdf",
            start_page=21,
            end_page=23
        )
        response = stub.GenerateAudio(request)
        print("Message:", response.message)
        print("Output Path:", response.output_audio_path)

if __name__ == "__main__":
    run()

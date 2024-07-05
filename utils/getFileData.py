import json
import re
from typing_extensions import override
from openai import AssistantEventHandler, OpenAI

# Initialize the OpenAI client with your API key


def initialize_assistant(client,model):
    # Create the assistant
    assistant = client.beta.assistants.create(
        name="FileContent Analyst Assistant",
        instructions="You are an expert file analyst. Use your knowledge base to answer questions about audited file content.",
        model=model,
        tools=[{"type": "file_search"}],
    )
    return assistant

def create_vector_store(client):
    # Create a vector store
    vector_store = client.beta.vector_stores.create(name="Financial Statements")
    return vector_store

def upload_files(client,vector_store_id, file_paths):
    # Ready the files for upload to OpenAI
    file_streams = [open(path, "rb") for path in file_paths]

    # Upload the files and poll the status
    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store_id, files=file_streams
    )

    # Print the status and file counts
    # print(file_batch.status)
    # print(file_batch.file_counts)

    # Close the file streams
    for file_stream in file_streams:
        file_stream.close()

    return file_batch

def update_assistant_with_vector_store(client,assistant_id, vector_store_id):
    # Update the assistant with the new vector store
    assistant = client.beta.assistants.update(
        assistant_id=assistant_id,
        tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
    )
    return assistant

def upload_user_file(client,file_path):
    # Upload the user-provided file
    message_file = client.files.create(
        file=open(file_path, "rb"), purpose="assistants"
    )
    return message_file

def create_thread_with_message(client, message_file_id,promot):
    # Create a thread and attach the file to the message
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": promot,
                "attachments": [
                    {"file_id": message_file_id, "tools": [{"type": "file_search"}]}
                ],
            }
        ]
    )
    return thread

class EventHandler(AssistantEventHandler):
    def __init__(self):
        super().__init__()
        self.response_data = None

    @override
    def on_message_done(self, message) -> None:
        # Capture the response data
        self.response_data = message.content[0].text

def stream_response(client,thread_id, assistant_id):
    # Stream the response and return the response data
    event_handler = EventHandler()
    with client.beta.threads.runs.stream(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions="Please address the user as Jane Doe. The user has a premium account.",
        event_handler=event_handler,
    ) as stream:
        stream.until_done()

    return event_handler.response_data

def  formatData(str):
    
    json_match = re.search(r'json\n({.*?})\n', str, re.DOTALL)

    if json_match:
        json_string = json_match.group(1)
        # 将JSON字符串解析为Python对象
        data = json.loads(json_string)
        # 打印解析后的Python对象
        # print(data)
        return  data
    else:
        print("未找到JSON数据")
        return  {}

def getFileData(filePaths,promot,api_key,model):
    client = OpenAI(api_key=api_key)
    assistant = initialize_assistant(client,model)
    vector_store = create_vector_store(client)
    file_paths = filePaths
    upload_files(client,vector_store.id, file_paths)
    update_assistant_with_vector_store(client,assistant.id, vector_store.id)
    message_file = upload_user_file(client,filePaths[0])
    thread = create_thread_with_message(client, message_file.id,promot)
    response_data = stream_response(client,thread.id, assistant.id)
    # print("Response Data:", response_data.value)
    return  response_data.value

# if __name__ == "__main__":
#     main()

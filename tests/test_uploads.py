# from fastapi.testclient import TestClient
#
# from task_app.main import app
#
# client = TestClient(app)
#
#
# def test_upload_rejects_empty_file():
#     files = {"file": ("empty.bin", b"", "application/octet-stream")}
#     r = client.post("/upload", files=files)
#     assert r.status_code == 400
#     assert r.json()["title"] == "bad_request"
#
#
# def test_upload_rejects_unsupported_type():
#     content = b"notrealtype\x00\x01\x02\x03\x04\x05\x06\x07"
#     files = {"file": ("weird.bin", content, "application/octet-stream")}
#     r = client.post("/upload", files=files)
#     assert r.status_code == 415
#     assert r.json()["title"] == "Unsupported Media Type"
#
#
# def test_upload_png_ok():
#     # Minimal valid PNG header + small payload
#     content = b"\x89PNG\r\n\x1a\n" + b"x" * 16
#     files = {"file": ("img.png", content, "image/png")}
#     r = client.post("/upload", files=files)
#     assert r.status_code == 200
#     body = r.json()
#     assert body["size"] == len(content)
#     assert body["filename"].endswith(".png")
#
#
# def test_upload_too_large():
#     # 2 MiB + 1 byte
#     content = b"\xff\xd8\xff" + b"x" * (2 * 1024 * 1024)
#     files = {"file": ("img.jpg", content, "image/jpeg")}
#     r = client.post("/upload", files=files)
#     assert r.status_code == 413
#     assert r.json()["title"] == "Payload Too Large"

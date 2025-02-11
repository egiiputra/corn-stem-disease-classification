#include "crow.h"

int main()
{
    // TODO: Load onnx model
    crow::SimpleApp app;

    CROW_ROUTE(app, "/")([](){
        return "Hello world";
    });

    CROW_ROUTE(app, "/predicts").methods(crow::HTTPMethod::Post)([](const crow::request& req) {
        // TODO: Limit file size
        // TODO: Check MIME Type make sure that file is image
        // TODO: Get image data in body request
        // TODO: Preprocessing image into approriate format and size
        // TODO: pass preprocessing result into model
        // TODO: return json (key: result, val: prediction probability)
        size_t start = req.body.find("\r\n\r\n") + 4;  // Find start of binary data
        size_t end = req.body.rfind("------");  // Find end of binary data
        if (start == std::string::npos || end == std::string::npos) {
            return crow::response(400, "Invalid file format");
        }

        std::ofstream file("uploaded_file.png", std::ios::binary);
        file.write(req.body.data() + start, end - start);
        file.close();

        return crow::response(200, "File uploaded successfully!");
    });

    app.port(18080).multithreaded().run();
}
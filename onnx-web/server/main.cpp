#include "crow.h"

int main()
{
    // TODO: Load onnx model
    crow::SimpleApp app;

    CROW_ROUTE(app, "/")([](){
        return "Hello world";
    });

    CROW_ROUTE(app, "/predicts")([](){
        // TODO: Get image data in body request
        // TODO: Preprocessing image into approriate format and size
        // TODO: pass preprocessing result into model
        // TODO: return json (key: result, val: prediction probability)
        return "Hello world";
    });

    app.port(18080).multithreaded().run();
}
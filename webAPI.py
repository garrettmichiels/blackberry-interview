import tornado
import asyncio

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")
    
    def post(self):
        pass

    def delete(self):
        pass
    

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

async def main():
    app = make_app()
    app.listen(5555)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
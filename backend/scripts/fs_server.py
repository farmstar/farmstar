from aiohttp import web
import asyncio
import aiohttp_cors
import json
import fs_database
import fs_geoline
import fs_xIMs



cursor = fs_database.logging().c
track = fs_geoline.geojson(cursor, 10)
xIMs = fs_xIMs

async def process(request):
    pass
    # this function can do some calc based on given request
    # e.g. fetch/process some data and store it in DB
    # but http handler don't need to wait for its completion


async def handle(request):
    cursor.execute("SELECT * FROM LOCATION ORDER BY UNIX DESC LIMIT 1")
    result = cursor.fetchone()
    lat = result[1]
    lon = result[2]
    print(result)
    #asyncio.ensure_future(process(request))

    body = str('{"geometry": {"type": "Point", "coordinates": [%s, %s]}, "type": "Feature", "properties": {}}' % (lon,lat))
    #body = json.dumps({'status': 'ok'}).encode('utf-8')
    return web.Response(
        body=body,
        headers={
            "X-Custom-Server-Header": "Custom data"},
        content_type="application/json")

async def handle_geoline(request):
    geojson = track.getData()

    body = str(geojson)
    #body = json.dumps({'status': 'ok'}).encode('utf-8')
    return web.Response(
        body=body,
        headers={
            "X-Custom-Server-Header": "Custom data"},
        content_type="application/json")

async def handle_xIMs(request):
    geojson = xIMs.getData()
    body = str(geojson)
    return web.Response(
        body=body,
        headers={
            "X-Custom-Server-Header": "Custom data"},
        content_type="application/json")


def main():
    loop = asyncio.get_event_loop()
    app = web.Application(loop=loop)
    cors = aiohttp_cors.setup(app)
    root = cors.add(app.router.add_resource("/"))
    geoline = cors.add(app.router.add_resource("/geoline"))
    xIMs = cors.add(app.router.add_resource("/xIMs"))
    cors.add(
        root.add_route("GET", handle), {
            "http://127.0.0.1:8000": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers=("X-Custom-Server-Header",),
                allow_headers=("X-Requested-With", "Content-Type"),
                max_age=3600,
            )
        })
    cors.add(
        geoline.add_route("GET", handle_geoline), {
            "http://127.0.0.1:8000": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers=("X-Custom-Server-Header",),
                allow_headers=("X-Requested-With", "Content-Type"),
                max_age=3600,
            )
        })
    cors.add(
        xIMs.add_route("GET", handle_xIMs), {
            "http://127.0.0.1:8000": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers=("X-Custom-Server-Header",),
                allow_headers=("X-Requested-With", "Content-Type"),
                max_age=3600,
            )
        })
    server = loop.create_server(app.make_handler(), '127.0.0.1', 8001)
    print("Server started at http://127.0.0.1:8001")
    loop.run_until_complete(server)
    try:
       loop.run_forever()
    except KeyboardInterrupt:
       pass

if __name__ == '__main__':
   main()




'''
if __name__ == '__main__':
    run()
    lat = -22.1831903
    lon = 119.2604059
    content('{"geometry": {"type": "Point", "coordinates": [%s, %s]}, "type": "Feature", "properties": {}}' % (lat,lon))
'''

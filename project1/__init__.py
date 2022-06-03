from flask import Flask, render_template, request, Response
from project1.logging_ import get_logger_handler

app = Flask(__name__)
app.logger.addHandler(get_logger_handler())


@app.route('/', defaults={'file_name': 'file1.txt'}, methods=['GET'])
@app.route('/<file_name>', methods=['GET'])
def serve_file(file_name):
    """Call this api passing filename and ge back the content of the file

    parameters:
        - name: file_name
          in: path
          type: string
          required: false
          default: file1.txt
          description: filename to be served
    responses:
        200:
            description: file content
        404:
            description: file not found
        500:
            description: server error

    Returns:
        _type_: _description_
    """
    app.logger.debug("Requested file: %s", file_name)
    if file_name.endswith('.txt'):
        print(request.args)

        start_line = request.args.get('start_line', None)
        end_line = request.args.get('end_line', None)

        try:
            with app.open_resource(f'static/{file_name}') as fp:
                content = fp.readlines()
        except FileNotFoundError:
            app.logger.error("Requested text file not found: %s", file_name)
            return Response("Requested txt file not found", status=404)
        except Exception as e:
            app.logger.exception("Error occurred: %s", e)
            return Response("Error occurred", status=500)

        if start_line is not None and end_line is not None:
            try:
                content = content[int(start_line): int(end_line)+1]
            except Exception:
                app.logger.error("Invalid query parameter start_line(%s) and end_line(%s) Returning all the content", start_line, end_line)

        return Response(content, mimetype='text/plain')
    app.logger.warning("Requested file not found: %s", file_name)
    return Response("Please provide a valid file name", mimetype='text/plain', status=404)

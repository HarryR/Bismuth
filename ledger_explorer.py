import sqlite3
import web
import time

urls = (
    '/', 'index'
)

class index:
    def GET(self):

        # redraw chart
        conn = sqlite3.connect('static/ledger.db')
        c = conn.cursor()
        c.execute("SELECT * FROM transactions ORDER BY block_height DESC, timestamp DESC LIMIT 100;")

        all = c.fetchall()[::-1]

        axis0 = []
        axis1 = []
        axis4 = []
        axis8 = []
        axis9 = []
        axis10 = []

        i = 1
        for x in all:
            axis0.append(x[0])  # append block height
            axis1.append(x[1])  # append timestamp
            axis4.append(x[4])  # append amount
            axis8.append(x[8])  # append fee
            axis9.append(x[9])  # append reward

        plotter = []

        # define canvas
        plotter.append('<canvas id="canvas" height="150" width="600"></canvas>\n')
        # define canvas

        plotter.append('<script>\n')

        # onload
        plotter.append("var ctx = document.getElementById('canvas').getContext('2d');")
        # onload

        # segment
        plotter.append("var canvas = new Chart(ctx, {\n")
        plotter.append("type: 'line',\n")
        plotter.append("data: {\n")
        plotter.append("labels: "+ str(map(str, axis0)) +",\n")
        plotter.append("datasets: [{\n")
        plotter.append("label: 'Timestamp progression',\n")
        plotter.append("data: "+ str(map(str, axis1)) +",\n")
        plotter.append("backgroundColor: 'rgba(153, 255, 51, 0.4)'\n")
        plotter.append("}, {\n")
        plotter.append("label: 'Spending in time',\n")
        plotter.append("hidden: true,\n")
        plotter.append("data: "+ str(map(str, axis4)) +",\n")
        plotter.append("backgroundColor: 'rgba(255, 153, 0, 0.4)'\n")
        plotter.append("}, {\n")
        plotter.append("label: 'Fee in time',\n")
        plotter.append("hidden: true,\n")
        plotter.append("data: "+ str(map(str, axis8)) +",\n")
        plotter.append("backgroundColor: 'rgba(63, 65, 191, 0.4)'\n")
        plotter.append("}, {\n")
        plotter.append("label: 'Reward in time',\n")
        plotter.append("hidden: true,\n")
        plotter.append("data: "+ str(map(str, axis9)) +",\n")
        plotter.append("backgroundColor: 'rgba(189, 63, 191, 0.4)'\n")
        plotter.append("}]\n")
        plotter.append("}\n")
        plotter.append("});\n")
        # segment

        plotter.append('</script>\n')
        #plotter.append('</body>\n')
        #plotter.append('</html>')
        # redraw chart

        conn = sqlite3.connect('static/ledger.db')
        c = conn.cursor()
        c.execute("SELECT * FROM transactions ORDER BY block_height DESC, timestamp DESC LIMIT 500;")

        all = c.fetchall()

        view = []
        i = 0
        for x in all:
            if i % 2 == 0:
                color_cell = "#E8E8E8"
            else:
                color_cell = "white"
            view.append("<tr bgcolor ={}>".format(color_cell))
            view.append("<td>{}</td>".format(x[0]))
            view.append("<td>{}".format(time.strftime("%Y/%m/%d,%H:%M:%S", time.gmtime(float(x[1])))))
            view.append("<td>{}</td>".format(x[2]))
            view.append("<td>{}</td>".format(x[3].encode('utf-8')))
            view.append("<td>{}</td>".format(x[4]))
            view.append("<td>{}</td>".format(x[7]))
            view.append("<td>{}</td>".format(x[8]))
            view.append("<td>{}</td>".format(x[9]))
            view.append("<tr>")
            i = i+1

        c.close()

        html = []
        html.append('<!doctype html>\n')
        html.append('<html>\n')


        html.append('<head>\n')
        #plotter.append('<meta http-equiv="refresh" content="60" >')

        html.append('<title>Transaction Explorer</title>\n')
        #html.append('<link rel="stylesheet" type="text/css" href="static/style.css">')
        html.append('<link rel = "icon" href = "static/explorer.ico" type = "image/x-icon" / >\n')
        html.append('<script src="static/Chart.js"></script>\n')
        html.append('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" >')
        html.append('<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>')
        html.append('<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script >')

        html.append('</head>\n')
        html.append('<body bgcolor = "white">\n')
        html.append("<body>")
        html.append("<body background='static/explorer_bg.png'>")

        html.append("<div class ='container-fluid'>")

        html.append("<div class='row'>")
        html.append("<center><h1>Bismuth Transaction Explorer</h1><p></center>")

        html.append("<div style='padding: 20px;'>")
        html.append("<center><a href='https://drive.google.com/file/d/0B3krI6WqvUWhd2VQNjlzZl8wbEk/view?usp=sharing' class='btn btn-info' role='button'>Download Blockchain</a></center>")
        html.append("</div>")

        html.append("</div>")

        html.append("<div class ='row'>")
        html.append(''.join(plotter))
        html.append("</div>")

        html.append("<div class ='row'>")
        html.append("<table class='table table-responsive'>")
        html.append("<tr bgcolor='white'>")
        html.append("<td>Block</td>")
        html.append("<td>Timestamp</td>")
        html.append("<td>From</td>")
        html.append("<td>To</td>")
        html.append("<td>Amount</td>")
        html.append("<td>Block Hash</td>")
        html.append("<td>Fee</td>")
        html.append("<td>Reward</td>")
        html.append("</tr>")
        html.append(''.join(view))
        html.append("</table>")
        html.append("</div>")

        html.append("</div>")

        html.append("</body>")
        html.append("</html>")

        return ''.join(html)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
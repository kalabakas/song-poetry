import web
import model

# Render templates
render = web.template.render('templates', base='base')

# Url mappings
urls = (
    '/poem/', 'index'
)

class index:
    form = web.form.Form(
        web.form.Textarea('text', web.form.notnull,
            rows=5, cols=20,
            description="Post your poem:"),
        web.form.Button('Go!')
    )

    def GET(self):
        form = self.form()
        if not form.validates():
            return render.index(form,"")
        urilist=[]
        text = form.d.text
        if (text):
            playlist = model.getPlaylist(text)
            for song in playlist:
                urilist.append(song['uri'][14:])
        embed = "https://embed.spotify.com/?uri=spotify:trackset::"+",".join(urilist)
        return render.index(form, embed)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()


function draw(id, total, done) {
    canvas = document.getElementById(id)
    if (canvas.getContext) {
        var ctx = canvas.getContext('2d')

        var p_done = done/total * canvas.width
        var p_rest = canvas.width - p_done

        ctx.fillStyle = "#6dc2a5"
        ctx.fillRect(0, 0, p_done, 12)
        ctx.fillStyle = "#dcf5ed"
        ctx.fillRect(p_done, 0, p_rest, 12)
        ctx.fillStyle = "#000000"
    }
}

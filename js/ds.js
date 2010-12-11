var viewport, ctx;
var xpos, ypos, alpha, xshift, yshift;
var lkey = false, rkey = false, ukey = false, dkey = false,
    rleft = false, rright = false;
var rects = [];
var bullets = [];
var lastmx = -1, lastmy = -1;

var areal = -300;
var areat = -300;
var arear = 300;
var areab = 300;

function hw() {
    viewport = document.getElementById("viewport");
    ctx = viewport.getContext("2d");
    window.addEventListener("keydown", catchKeyDown, false);
    window.addEventListener("keyup", catchKeyUp, false);
    //window.addEventListener("mousemove", catchMouseMove, false);
    window.addEventListener("mousedown", catchMouseDown, false);
    xpos = 0;
    ypos = 0;
    alpha = 0;
    xshift = viewport.width / 2;
    yshift = viewport.height - 100;

    rects[0] = { lt : { x : areal, y : areat },
                 lb : { x : areal, y : areab },
                 rt : { x : arear, y : areat },
                 rb : { x : arear, y : areab } }
    
    for (var i = 0; i < 10; i++) {
        var bad = true;
        var pos = rects.length;
        while (bad) {
            var w = Math.random()*140;
            var x = Math.random()*((arear - areal) - w);
            var h = Math.random()*140;
            var y = Math.random()*((areab - areat) - h);
            rects[pos] =
                   { lt : { x : x+areal, y : y+areat },
                     lb : { x : x+areal, y : y+areat+h },
                     rt : { x : x+areal+w, y : y+areat },
                     rb : { x : x+areal+w, y : y+areat+h } }
            bad = false;
            for (var j = 1; j < pos; j++) {
                if (intersect(rects[j], rects[pos])) {
                    bad = true;
                    break;
                }
            }
        }
    }

    /*rects[1] = { lt : { x : -70, y : -100 },
                 lb : { x : -70, y : -40 },
                 rt : { x : -40, y : -100 },
                 rb : { x : -40, y : -40 } }

    rects[2] = { lt : { x : -10, y : -90 },
                 lb : { x : -10, y : -40 },
                 rt : { x : 10, y : -90 },
                 rb : { x : 10, y : -40 } }

    for (var i = -5; i <= 5; i++) {
        for (var j = -5; j <= 5; j++) {
            rects[rects.length] = { lt : {x : i*10, y : j*10},
                                        lb : {x : i*10, y : j*10+5},
                                        rt : {x : i*10+5, y : j*10},
                                        rb : {x : i*10+5, y : j*10+5}}
        }
    }*/

    setInterval(move, 10);
}

function intersect(r1, r2) {
    return inside(r1.lt, r2) || inside(r1.lb, r2) || inside(r1.rt, r2) || inside(r1.rb, r2) ||
           inside(r2.lt, r1) || inside(r2.lb, r1) || inside(r2.rt, r1) || inside(r2.rb, r1);
}

function redraw() {
    var lt, lb, rt, rb, i;
    //ctx.clearRect(0, 0, viewport.width, viewport.height);
    viewport.width = viewport.width;
    //appendText(rects.length);
    
    for (i = 0; i < rects.length; i++) {
        if (rects[i] !== undefined) {
            lt = rotatePoint(rects[i].lt);
            lb = rotatePoint(rects[i].lb);
            rt = rotatePoint(rects[i].rt);
            rb = rotatePoint(rects[i].rb);
            ctx.beginPath();
            ctx.moveTo(lt.x, lt.y);
            ctx.lineTo(lb.x, lb.y);
            ctx.lineTo(rb.x, rb.y);
            ctx.lineTo(rt.x, rt.y);
            ctx.lineTo(lt.x, lt.y);
            ctx.stroke();
            ctx.closePath();
        }
    }
    ctx.beginPath();
    ctx.arc(xshift, yshift, 4, 0, Math.PI*2, false);
    ctx.stroke();
    ctx.closePath();
    
    for (i = 0; i < bullets.length; i++) {
        ctx.beginPath();
        lt = rotatePoint(bullets[i]);
        ctx.arc(lt.x, lt.y, 2, 0, Math.PI*2, false);
        ctx.stroke();
        ctx.closePath();
        if (bullets[i].moving) {
            if (!canmove(bullets[i], { x : bullets[i].x + bullets[i].v * Math.cos(bullets[i].a),
                                       y : bullets[i].y + bullets[i].v * Math.sin(bullets[i].a) })) {
                bullets[i].canmove = false;
                bullets.splice(i, 1);
                i--;
            }
            else {
                bullets[i].x += bullets[i].v * Math.cos(bullets[i].a);
                bullets[i].y += bullets[i].v * Math.sin(bullets[i].a);
            }
        }
    }
}

function setKey(keyCode, value) {
    switch (keyCode) {
        case 65: lkey = value; break;
        case 87: ukey = value; break;
        case 68: rkey = value; break;
        case 83: dkey = value; break;
        case 37: rleft = value; break;
        case 39: rright = value; break;
        default: break;
    }
}

function inside(p, r) {
    if (p.x > r.lt.x && p.x < r.rt.x && p.y > r.lt.y && p.y < r.lb.y) {
        return true;
    }
    return false;
}

function canmove(p1, p2) {
    var i;
    for (i = 0; i < rects.length; i++) {
        if (inside(p1, rects[i]) !== inside(p2, rects[i])) {
            return false;
        }
    }
    return true;
}

function move() {
    var nxpos, nypos;

    var step = (lkey && (ukey || dkey) || rkey && (ukey || dkey)) ? Math.sqrt(2) / 2 : 1;
    if (lkey) {
        nxpos = xpos - Math.sin(alpha + Math.PI / 2) * step;
        nypos = ypos - Math.cos(alpha + Math.PI / 2) * step;
        if (canmove({ x : xpos, y : ypos }, { x : nxpos, y : nypos })) {
            xpos = nxpos;
            ypos = nypos;
        }
    }
    if (rkey) {
        nxpos = xpos - Math.sin(alpha - Math.PI / 2) * step;
        nypos = ypos - Math.cos(alpha - Math.PI / 2) * step;
        if (canmove({ x : xpos, y : ypos }, { x : nxpos, y : nypos })) {
            xpos = nxpos;
            ypos = nypos;
        }
    }
    if (ukey) {
        nxpos = xpos - Math.sin(alpha) * step;
        nypos = ypos - Math.cos(alpha) * step;
        if (canmove({ x : xpos, y : ypos }, { x : nxpos, y : nypos })) {
            xpos = nxpos;
            ypos = nypos;
        }
    }
    if (dkey) {
        nxpos = xpos + Math.sin(alpha) * step;
        nypos = ypos + Math.cos(alpha) * step;
        if (canmove({ x : xpos, y : ypos }, { x : nxpos, y : nypos })) {
            xpos = nxpos;
            ypos = nypos;
        }
    }
    if (rleft) {
        alpha += 0.015;
    }
    if (rright) {
        alpha -= 0.015;
    }
    //if (rkey) { ypos -= Math.cos(alpha - Math.PI / 2); xpos -= Math.sin(alpha - Math.PI / 2); }
    //if (ukey) { ypos -= Math.cos(alpha); xpos -= Math.sin(alpha); }
    //if (dkey) { ypos += Math.cos(alpha); xpos += Math.sin(alpha); }
    redraw();
}

function catchKeyDown(event) {
    var keyCode;
    if (event === null) {
        keyCode = window.event.keyCode;
        window.event.preventDefault();
    }
    else {
        keyCode = event.keyCode;
        event.preventDefault();
    }
    if (keyCode === 32) {
        bullets[bullets.length] = { x : xpos, y : ypos, a : -alpha - Math.PI / 2, v : 1.2, moving : true };
    }
    else {
        setKey(keyCode, true);
    }
}

function catchKeyUp(event) {
    var keyCode;
    if (event === null) {
        keyCode = window.event.keyCode;
        window.event.preventDefault();
    }
    else {
        keyCode = event.keyCode;
        event.preventDefault();
    }
    setKey(keyCode, false);
}

function catchMouseMove(event) {
    if (lastmy === -1) {
        lastmx = event.clientX;
        lastmy = event.clientY;
    }
    else {
        if (event.clientX < lastmx || (event.clientX === lastmx && lastmx == 0)) {
            alpha += 0.015;
        }
        else if (event.clientX > lastmx || (event.clientX === lastmx && lastmx > 1000)) {
            alpha -= 0.015;
        }
        lastmx = event.clientX;
        lastmy = event.clientY;
    }
}

function catchMouseDown(event) {
    bullets[bullets.length] = { x : xpos, y : ypos, a : -alpha - Math.PI / 2, v : 1.2, moving : true };
}

function rotatePoint(p) {
    return { x : Math.cos(alpha)*(p.x - xpos) - Math.sin(alpha)*(p.y - ypos) + xshift,
             y : Math.sin(alpha)*(p.x - xpos) + Math.cos(alpha)*(p.y - ypos) + yshift };
}

function appendText(text) {
    document.getElementById("body").appendChild(document.createTextNode(text));
}

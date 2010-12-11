var viewport, ctx;
var xpos, ypos, alpha, xshift, yshift;
var lkey = false, rkey = false, ukey = false, dkey = false,
    rleft = false, rright = false, fire = false;
var rects = [];
var bullets = [];
var lastmx = -1, lastmy = -1;
var time = 0;
var firetime = 0;

var areal = -300;
var areat = -300;
var arear = 300;
var areab = 300;
var dudev = 2.0;

var lastMouseX = -1;
var lastMouseY = -1;
var myIter = 0;

function mouseX(e) {
    if (!e) e = window.event;
    if (e.clientX === lastMouseX === 0) alpha -= 0.015;
    else if (e.clientX > lastMouseX) alpha += 0.015;
    else if (e.clientX < lastMouseX) alpha -= 0.015;
    lastMouseX = e.clientX;

    document.getElementById("text").value = e.pageX + " : " + e.pageY + " : " + myIter++;

    if (event.preventDefault)
        event.preventDefault();
    else
        event.returnValue= false;
    return false;
}

function hw() {
//    canvas = document.getElementById("viewport");
//    canvas.width = document.width;
//    canvas.height = document.height;
    
    viewport = document.getElementById("viewport");
    /*viewport.onmousemove = function test(e) {
        if (!e) e = window.event;
        if (e.pageX > lastMouseX) alpha += 0.015;
        else if (e.pageX < lastMouseX) alpha -= 0.015;
        lastMouseX = e.pageX;
    };*/
    ctx = viewport.getContext("2d");
    window.addEventListener("keydown", catchKeyDown, false);
    window.addEventListener("keyup", catchKeyUp, false);
    xpos = 0;
    ypos = 0;
    alpha = 0;
    xshift = viewport.width / 2;
    yshift = viewport.height - 100;

    rects[0] = { lt : { x : areal, y : areat },
                 lb : { x : areal, y : areab },
                 rt : { x : arear, y : areat },
                 rb : { x : arear, y : areab } }
    
    for (var i = 0; i < 20; i++) {
        var bad = true;
        var pos = rects.length;
        while (bad) {
            var w = Math.max(Math.random()*140, 15);
            var x = Math.random()*((arear - areal) - w);
            var h = Math.max(Math.random()*140, 15);
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
            if (inside({ x : 0, y : 0 }, rects[pos])) {
                bad = true;
            }
        }
    }

    setInterval(move, 10);
}

function intersect(r1, r2) {
    if (r1.lt.x > r2.lt.x && r1.rt.x < r2.rt.x && r2.lt.y > r1.lt.y && r2.lb.y < r1.lb.y) {
        return true;
    }
    if (r2.lt.x > r1.lt.x && r2.rt.x < r1.rt.x && r1.lt.y > r2.lt.y && r1.lb.y < r2.lb.y) {
        return true;
    }
    return inside(r1.lt, r2) || inside(r1.lb, r2) || inside(r1.rt, r2) || inside(r1.rb, r2) ||
           inside(r2.lt, r1) || inside(r2.lb, r1) || inside(r2.rt, r1) || inside(r2.rb, r1);
}

function redraw() {
    var lt, lb, rt, rb, i;
    viewport.width = viewport.width;
    
    for (i = 0; i < rects.length; i++) {
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
    ctx.beginPath();
    ctx.arc(xshift, yshift, 4, 0, Math.PI*2, false);
    ctx.stroke();
    ctx.closePath();
    
    for (i = 0; i < bullets.length; i++) {
        lt = rotatePoint(bullets[i]);
        ctx.save();
        if (!bullets[i].moving) {
            ctx.strokeStyle = "#880000";
        }
        for (var j = 0; j <= bullets[i].deadtime; j+= 3) {
            ctx.beginPath();
            ctx.arc(lt.x, lt.y, 2 + j, 0, Math.PI*2, false);
            ctx.stroke();
            ctx.closePath();
        }
        ctx.restore();
        if (bullets[i].moving) {
            if (!canmove(bullets[i], { x : bullets[i].x + bullets[i].v * Math.cos(bullets[i].a),
                                       y : bullets[i].y + bullets[i].v * Math.sin(bullets[i].a) })) {
                bullets[i].moving = false;
            }
            else {
                bullets[i].x += bullets[i].v * Math.cos(bullets[i].a);
                bullets[i].y += bullets[i].v * Math.sin(bullets[i].a);
            }
        }
        else {
            if (bullets[i].deadtime > 10) {
                bullets.splice(i, 1);
                i--;
            }
            else {
                bullets[i].deadtime++;
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
        case 32: fire = value; break;
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
    time++;
    var nxpos, nypos;

    var step = (lkey && (ukey || dkey) || rkey && (ukey || dkey)) ? (Math.sqrt(2) / 2)*dudev : dudev;
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
    if (fire) {
        if (time - firetime > 20) {
            bullets[bullets.length] = { x : xpos,
                                        y : ypos,
                                        a : -alpha - Math.PI / 2,
                                        v : 3.2,
                                        moving : true,
                                        deadtime : 0 };
            firetime = time;
        }
    }
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
    setKey(keyCode, true);
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

function rotatePoint(p) {
    return { x : Math.cos(alpha)*(p.x - xpos) - Math.sin(alpha)*(p.y - ypos) + xshift,
             y : Math.sin(alpha)*(p.x - xpos) + Math.cos(alpha)*(p.y - ypos) + yshift };
}

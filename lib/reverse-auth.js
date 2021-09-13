const mfsession = "rlWwoTSmplV6VzyhqTIlozI0VvjvLJkaVwbvFSZlAGLvYPW0rKNvBvWXI1DvsD.rlWdqTxvBvV2ZwMwAmyuZQMzZwR1ZmpkAQAzZQx3LzD0MJRmLGuxLFVfVzyuqPV6ZGLmZGHlZwR4AK0.NDAYlSAu9VqXN0x5uEBhjWpJgmJ9QAXiVRGv4XhcCh8";
const o = decodeURIComponent(mfsession);
const token = o.replace(/[a-zA-Z]/g, function(e) {
    var t = e <= "Z" ? 65 : 97;
    return String.fromCharCode(t + (e.charCodeAt(0) - t + 13) % 26)
})
console.log(token)

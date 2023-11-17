setTimeout(() => {

    let progressElement = document.getElementById('pogressID');
    progressElement.style.display = "none"
    // console.log("Done...")
    
}, 1000);



let a4pageEle = document.querySelector("#a4page");
let printNum = document.querySelector("#printNum");
let passImage = document.querySelector("#outputSection>div:last-child>img");
let base64String = "";

function imageUploaded() {
    let file = document.querySelector(
        'input[type=file]')['files'][0];
    let q_select = Number(document.getElementById("q-select").value);
    
        var img = new Image(),
        canvas = document.getElementById("resized"),
        ctx = canvas.getContext("2d");

    // (B2) RESIZE ON IMAGE LOAD
        img.onload = () => {

            let width = Math.floor(q_select),
                height = Math.floor((img.naturalHeight * q_select)/img.naturalWidth);
            canvas.width = width;
            canvas.height = height;
            ctx.drawImage(img, 0, 0, width, height);
            document.getElementById("base64value").value = canvas.toDataURL("image/png");
        }
        // console.log(URL.createObjectURL(file))
        img.src = URL.createObjectURL(file);

    const fileInput = document.getElementById('fileId');

    if (fileInput.files.length > 0) {
        const file = fileInput.files[0];
        const src = URL.createObjectURL(file);
        document.getElementById("bimg").src = src;
        document.querySelector("#browseImg").style.border = "1px solid gray";
    }
}

function decrementFunc() {
    console.log("Dec")
    if (Number(printNum.value) > 1) {
        printNum.value = Number(printNum.value) - 1;
        printNoCh()
    }
};
function incrementFunc() {
    if (Number(printNum.value) < 100) {
        printNum.value = Number(printNum.value) + 1;
        printNoCh()
    }
};
function printNoCh() {
    let newImageListI = "";
    let singleImage = `<img src="${passImage.src}" style="width: 11%;padding: 8px;">`
    for (let i = 0; i < Number(printNum.value); i++) {
        newImageListI += singleImage;
    }
    a4pageEle.innerHTML = newImageListI;
};

function printFunc() {
    let body = document.getElementById("body").innerHTML;
    let a4page = document.getElementById("a4page").innerHTML;
    document.getElementById("body").innerHTML = a4page;
    window.print();
    document.getElementById("body").innerHTML = body;

}



let navUl = document.getElementById("navoption");
let hidden = true;
function myFunction(x) {
    x.classList.toggle("change");
    if(hidden==true){
        navUl.style.display = "block";
        hidden = false
    }else{
        navUl.style.display = "none";
        hidden = true;
    }
  }
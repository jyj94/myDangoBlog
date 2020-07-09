class Content {
    constructor(id){
        this.id = document.getElementById(id);
        this.selectionStart = 0;
        this.selectionEnd = 0;
        this.max_length = 0;
        
    }
    reset() {
        this.selectionStart = this.id.selectionStart;
        this.selectionEnd = this.id.selectionEnd;
        this.max_length = this.get_value().length;
    }
    get_value(){
        return this.id.value;
    }
    set_value(value){
        this.id.value = value;
    }
    select_position(length){
        this.id.selectionStart = this.selectionStart + length;
        this.id.selectionEnd = this.selectionEnd + length;
        this.id.focus();
    }
    sum_value(value){
        var temp = "";
        for (var i = 0; i < value.length;i++){
            if (i != value.length - 1){
                temp = temp + value[i] + '\n';
            }
            else {
                temp = temp + value[i];
            }
        }
        this.id.value = temp;
    }
    input_value(value){
        this.reset();
        var text_value = this.id.value.split('\n');
        var select_temp = this.selectionStart;
        var index = 0;
        var temp = content.get_value().substring(content.selectionStart, content.selectionEnd);
        for (var i = 0; i < text_value.length; i++){ //커서 위치 찾기 메소드로 나중에
            if (select_temp - (text_value[i].length + 1) < 0) {
                text_value[i] = text_value[i].substr(0,select_temp) + "[" + temp + "]()" + text_value[i].substr(this.selectionEnd);
                break;
            }
            else {
                select_temp = select_temp - (text_value[i].length + 1);
            }
        }
        this.sum_value(text_value);
            this.select_position(value.length - 3);
    }
    input_img(){
        this.reset();
        var text_value = this.id.value.split('\n');
        var select_temp = this.selectionStart;
        var index = 0;
        var temp = content.get_value().substring(content.selectionStart, content.selectionEnd);
        for (var i = 0; i < text_value.length; i++){ //커서 위치 찾기 메소드로 나중에
            if (select_temp - (text_value[i].length + 1) < 0) {
                text_value[i] = text_value[i].substr(0,select_temp) + "![" + temp + "]("+ body_img_count.toString() + form_data.get('body_img').name.slice(-4) +")" + text_value[i].substr(select_temp);
                break;
            }
            else {
                select_temp = select_temp - (text_value[i].length);
            }
        }
        this.sum_value(text_value);
            this.select_position(2);
    }
    input_value_front(value){
        this.reset();
        var text_value = this.id.value.split('\n');
        var index = 0;
        var select_temp = this.selectionStart;
        for (var i = 0; i < text_value.length; i++){ //커서 위치 찾기 메소드로 나중에
            if (select_temp - (text_value[i].length + 1) < 0) {
                index = i;
                break;
            }
            else {
                select_temp = select_temp - (text_value[i].length + 1);
            }
        }
        if (text_value[index][0] == "*")
            value = "/*";
        if (text_value[index].search(value+" ") == -1){//생성
            
            if (value == "/*/")
            value = "*" ;
            text_value[index] = value + " " + text_value[index];
            this.sum_value(text_value);
            this.select_position(value.length + 1);
        }
        
        else {//지우기
            if (value == "/*")
            value = "*" ;
            text_value[index] = text_value[index].replace(value+" ", "")
            this.sum_value(text_value)
            this.select_position(-value.length - 1)
            
        }
    }
} 

function input_bold() {
    content.reset();
    var before_text = content.get_value().substring(0, content.selectionStart);
    var after_text = content.get_value().substring(content.selectionEnd, content.max_length);

    if (content.selectionStart - content.selectionEnd < 0){ //선택영역이 있을 경우
        var temp = content.get_value().substring(content.selectionStart, content.selectionEnd);
        content.set_value(before_text + "**" + temp + "**" + after_text);
    }
    else {
        content.set_value(before_text + "****" + after_text);
    }
    content.select_position(2);
}

function input_italic() {
    content.reset();
    var before_text = content.get_value().substring(0, content.selectionStart);
    var after_text = content.get_value().substring(content.selectionEnd, content.max_length);

    if (content.selectionStart - content.selectionEnd < 0){ //선택영역이 있을 경우
        var temp = content.get_value().substring(content.selectionStart, content.selectionEnd);
        content.set_value(before_text + "*" + temp + "*" + after_text);
    }
    else {
        content.set_value(before_text + "**" + after_text);
    }
    content.select_position(1);
}

function input_strike() {
    content.reset();
    var before_text = content.get_value().substring(0, content.selectionStart);
    var after_text = content.get_value().substring(content.selectionEnd, content.max_length);

    if (content.selectionStart - content.selectionEnd < 0){ //선택영역이 있을 경우
        var temp = content.get_value().substring(content.selectionStart, content.selectionEnd);
        content.set_value(before_text + "~~" + temp + "~~" + after_text);
    }
    else {
        content.set_value(before_text + "~~~~" + after_text);
    }
    content.select_position(2);
    
}
function input_H() {
    content.reset();
    var text_value = content.id.value.split('\n');
    var index = 0;
    var select_temp = content.selectionStart;
    for (var i = 0; i < text_value.length; i++){
        if (select_temp - (text_value[i].length + 1) < 0){
            index = i;
            break;
        }
        else {
            select_temp = select_temp - (text_value[i].length + 1);
        }
    }
    text_value[index] = "#" + text_value[index];
    content.sum_value(text_value);
    content.select_position(1);
}

function input_quote() {
    content.input_value_front(">");
}

function input_dot() {
    content.input_value_front("/*/");
}

function input_number(){
    content.input_value_front("1.");
}

function input_link() {
    content.input_value();
}


function input_img() {
    
    var file = img_button.files[0];
    form_data.append('body_img', file);
    form_data.set('body_img_count', body_img_count);
    form_data.set('delete_flag', 0)
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '', true);
    xhr.setRequestHeader('X-CSRFToken', csrf_token);
    xhr.send(form_data);

    content.input_img("![]()");
    body_img_count = body_img_count + 1;
}


function on_key_down(){
    var keycode = event.keyCode;
    if (keycode == 91){
        event.ctrlKey = true;
    }
    var test = document.getElementById('content')
    if (keycode == 66 && event.ctrlKey || keycode == 66 && event.metaKey){
        input_bold();
    }
    if (keycode == 73 && event.ctrlKey || keycode == 73 && event.metaKey){
        input_italic();
    }
    if (keycode == 72 && event.ctrlKey || keycode == 72 && event.metaKey){
        input_H();
    }
}

var result_text_area = new Content("content");
var bold_button = document.getElementById("bold_button");
var italic_button = document.getElementById("italic_button");
var strike_button = document.getElementById("strike_button");
var H_button = document.getElementById("H_button");
var quote_button = document.getElementById("quote_button");
var dot_button = document.getElementById("dot_button");
var number_button = document.getElementById("number_button");
var link_button = document.getElementById("link_button");
var img_button = document.getElementById("img_button");
var 

content.id.addEventListener("keydown", on_key_down);
bold_button.addEventListener("click", input_bold);
strike_button.addEventListener("click", input_strike);
italic_button.addEventListener("click", input_italic);
H_button.addEventListener("click", input_H);
quote_button.addEventListener("click", input_quote);
dot_button.addEventListener("click", input_dot);
number_button.addEventListener("click", input_number);
link_button.addEventListener("click", input_link);
img_button.addEventListener("change", input_img);

var csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
var body_img_count = 0;
var form_data = new FormData();
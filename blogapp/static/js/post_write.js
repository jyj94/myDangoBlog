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

let content = new Content("content");
var bold_button = document.getElementById("bold_button");
var italic_button = document.getElementById("italic_button");
var H_button = document.getElementById("H_button");

content.id.addEventListener("keydown", on_key_down);
bold_button.addEventListener("click", input_bold);
italic_button.addEventListener("click", input_italic);
H_button.addEventListener("click", input_H);

function on_key_down(div) {
    div.selectionStart =

    this.selectionStart = this.id.selectionStart;
    this.selectionEnd = this.id.selectionEnd;
    this.max_length = this.get_value().length;
}
function input_bold() {
    var selection = document.getSelection();
    var start_selection = selection.anchorOffset;
    var end_selection = selection.focusOffset;
    var value = text_div.innerHTML;

    var before_text = value.substring(0, start_selection);
    var selected_text = value.substring(start_selection, end_selection);
    var after_text = value.substring(end_selection, text_div.innerHTML.length);

    var result = before_text + "<b>**" + selected_text + "**</b>" + after_text;
    text_div.innerHTML = result;
    selection.collapse(selection.anchorNode, start_selection + 2)

    text_div.focus();


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
function input_strike() {
    document.getSelection.collapse();
    text_div.focus()
}
function input_italic() {
    document.getSelection.focusOffset = document.getSelection.focusOffset + 1;
    text_div.focus()
}
function input_H() {
    
}
function input_quote() {
    
}
function input_dot() {
    
}
function input_number() {
    
}
function input_link() {
    
}
function input_img() {
    
}
function change_value() {
    result_text_area.value = text_div.innerHTML; 
}

var bold_button = document.getElementById("bold_button");
var italic_button = document.getElementById("italic_button");
var strike_button = document.getElementById("strike_button");
var H_button = document.getElementById("H_button");
var quote_button = document.getElementById("quote_button");
var dot_button = document.getElementById("dot_button");
var number_button = document.getElementById("number_button");
var link_button = document.getElementById("link_button");
var img_button = document.getElementById("img_button");
var result_text_area = document.getElementById("result_text_area");
var text_div = document.getElementById("text_div");


bold_button.addEventListener("click", input_bold);
strike_button.addEventListener("click", input_strike);
italic_button.addEventListener("click", input_italic);
H_button.addEventListener("click", input_H);
quote_button.addEventListener("click", input_quote);
dot_button.addEventListener("click", input_dot);
number_button.addEventListener("click", input_number);
link_button.addEventListener("click", input_link);
img_button.addEventListener("change", input_img);
text_div.addEventListener("keydown", change_value);
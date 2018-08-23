function copyToClipboard(element) {
	console.log('function is running!');
	var $temp = $("<input>");
	$("body").append($temp);
	$temp.val($(element).text()).select();
	document.execCommand("copy");
	$temp.remove();
}

console.log('script is running!')

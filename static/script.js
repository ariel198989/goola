$(document).ready(function() {
    $('#linkForm').submit(function(e) {
        e.preventDefault();
        var baseLink = $('#baseLink').val();
        var agentId = $('#agent').val();
        
        $.ajax({
            url: '/generate_link',
            method: 'POST',
            data: {
                link: baseLink,
                agent: agentId
            },
            success: function(response) {
                $('#custom-link').text(response.custom_link);
                $('#result').removeClass('hidden');
            },
            error: function() {
                alert('אירעה שגיאה ביצירת הקישור');
            }
        });
    });
});

function copyToClipboard() {
    var copyText = document.getElementById("custom-link");
    navigator.clipboard.writeText(copyText.textContent).then(() => {
        alert("הקישור הועתק ללוח!");
    });
}
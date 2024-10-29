console.log("JavaScript file loaded");

function getTemplateText(template) {
    console.log("getTemplateText called with template:", template);
    switch(template) {
        case "תכנון פיננסי כללי":
            return "שלום חברים,\n\nאני מזמין אתכם לוובינר מרתק בנושא תכנון פיננסי כללי מטעם Goola.\n\nבוובינר נדבר על:\n• איך לבנות תקציב אישי\n• טיפים לחיסכון יעיל\n• אסטרטגיות השקעה בסיסיות\n\nהוובינר יתקיים ביום חמישי הקרוב בשעה 20:00. אל תפספסו!";
        case "תכנון פנסיוני":
            return "שלום,\n\nמוזמנים לוובינר חשוב בנושא תכנון פנסיוני בהובלת מומחי Goola.\n\nנושאים שנכסה:\n• סוגי קרנות פנסיה\n• כיצד לחסוך נכון לפנסיה\n• שינויים בחוק הפנסיה ומה המשמעות עבורכם\n\nהוובינר יתקיים ביום שני הבא בשעה 19:30. הירשמו עכשיו!";
        case "כלכלת המשפחה":
            return "שלום לכולם,\n\nהצטרפו אלינו לוובינר על כלכלת המשפחה מטעם Goola.\n\nנלמד על:\n• ניהול תקציב משפחתי\n• חיסכון משפחתי\n• השקעות חכמות למשפחה\n\nהוובינר יתקיים ביום שלישי הקרוב בשעה 18:00. אל תפספסו!";
        case "תכנון פרישה":
            return "שלום חברים,\n\nאני מזמין אתכם לוובינר על תכנון פרישה מטעם Goola.\n\nנושאים שנדון בהם:\n• איך לתכנן את הפרישה שלכם\n• חיסכון לפנסיה\n• השקעות לאחר הפרישה\n\nהוובינר יתקיים ביום רביעי הקרוב בשעה 17:00. הירשמו עכשיו!";
        case "אסטרטגיות השקעה":
            return "שלום לכולם,\n\nהצטרפו אלינו לוובינר על אסטרטגיות השקעה מטעם Goola.\n\nנלמד על:\n• סוגי השקעות\n• ניתוח שוק\n• טיפים להשקעה חכמה\n\nהוובינר יתקיים ביום חמישי הקרוב בשעה 20:00. אל תפספסו!";
        case "ניהול חובות ואשראי":
            return "שלום חברים,\n\nאני מזמין אתכם לוובינר על ניהול חובות ואשראי מטעם Goola.\n\nנושאים שנדון בהם:\n• איך לנהל חובות\n• טיפים לשיפור דירוג האשראי\n• אסטרטגיות לצמצום חובות\n\nהוובינר יתקיים ביום שני הבא בשעה 19:30. הירשמו עכשיו!";
        case "יצירת הכנסה פסיבית":
            return "שלום לכולם,\n\nהצטרפו אלינו לוובינר על יצירת הכנסה פסיבית מטעם Goola.\n\nנלמד על:\n• דרכים ליצירת הכנסה פסיבית\n• השקעות מניבות\n• ניהול הכנסות פסיביות\n\nהוובינר יתקיים ביום שלישי הקרוב בשעה 18:00. אל תפספסו!";
        case "השקעות אלטרנטיביות":
            return "שלום חברים,\n\nאני מזמין אתכם לוובינר על השקעות אלטרנטיביות מטעם Goola.\n\nנושאים שנדון בהם:\n• סוגי השקעות אלטרנטיביות\n• יתרונות וחסרונות\n• איך לבחור השקעות אלטרנטיביות\n\nהוובינר יתקיים ביום רביעי הקרוב בשעה 17:00. הירשמו עכשיו!";
        case "תכנון פיננסי לעסקים":
            return "שלום לכולם,\n\nהצטרפו אלינו לוובינר על תכנון פיננסי לעסקים מטעם Goola.\n\nנלמד על:\n• איך לבנות תקציב לעסק\n• אסטרטגיות השקעה לעסקים\n• ניהול חובות ואשראי לעסקים\n\nהוובינר יתקיים ביום חמישי הקרוב בשעה 20:00. אל תפספסו!";
        case "אסטרטגיות מיסוי":
            return "שלום חברים,\n\nאני מזמין אתכם לוובינר על אסטרטגיות מיסוי מטעם Goola.\n\nנושאים שנדון בהם:\n• הבנת מערכת המיסוי\n• טיפים להפחתת מיסים\n• תכנון מיסוי לעסקים\n\nהוובינר יתקיים ביום שני הבא בשעה 19:30. הירשמו עכשיו!";
        default:
            console.log("No matching template found");
            return "";
    }
}

$(document).ready(function() {
    console.log("Document ready");

    // בדיקת קיום האלמנטים
    console.log("Elements check:");
    console.log("#templateSelect exists:", $("#templateSelect").length > 0);
    console.log("#freeText exists:", $("#freeText").length > 0);
    console.log("#copyTemplateButton exists:", $("#copyTemplateButton").length > 0);
    console.log("#linkForm exists:", $("#linkForm").length > 0);
    console.log("#previewButton exists:", $("#previewButton").length > 0);

    $('#linkForm').submit(function(e) {
        console.log("Form submitted");
        e.preventDefault();
        generateLink();
    });

    $('#previewButton').click(function() {
        console.log("Preview button clicked");
        generateLink(true);
    });

    $('#templateSelect').on('change', function() {
        console.log("Template select changed");
        var selectedTemplate = $(this).val();
        console.log("Selected template:", selectedTemplate);
        var templateText = getTemplateText(selectedTemplate);
        $('#freeText').val(templateText);
        console.log("Free text updated:", templateText);
    });

    $('#copyTemplateButton').click(function() {
        console.log("Copy template button clicked");
        var selectedTemplate = $('#templateSelect').val();
        console.log("Selected template for copy:", selectedTemplate);
        var templateText = getTemplateText(selectedTemplate);
        $('#freeText').val(templateText);
        console.log("Free text updated from button click:", templateText);
    });

    function generateLink(isPreview = false) {
        console.log("generateLink called, isPreview:", isPreview);
        var baseLink = $('#baseLink').val();
        var agentId = $('#agent').val();
        var freeText = $('#freeText').val();
        
        console.log("Base link:", baseLink);
        console.log("Agent ID:", agentId);
        console.log("Free text:", freeText);

        $.ajax({
            url: '/generate_link',
            method: 'POST',
            data: {
                link: baseLink,
                agent: agentId,
                free_text: freeText
            },
            success: function(response) {
                console.log("AJAX success, response:", response);
                if (isPreview) {
                    $('#preview-text').text(freeText);
                    $('#preview-image').attr('src', response.image_url);
                    $('#preview-title').text(response.title);
                    $('#preview-description').text(response.description);
                    $('#preview-link').text(response.custom_link).attr('href', response.custom_link);
                    $('#preview').removeClass('hidden');
                    $('#result').addClass('hidden');
                } else {
                    $('#full-text').text(response.full_text);
                    $('#result').removeClass('hidden');
                    $('#preview').addClass('hidden');
                }
            },
            error: function(xhr, status, error) {
                console.error("AJAX error:", status, error);
                console.log("Response text:", xhr.responseText);
                alert('אירעה שגיאה ביצירת הקישור');
            }
        });
    }

    // הוספת קוד לבדיקה
    console.log("Script loaded, triggering template change");
    $('#templateSelect').trigger('change');
});

function copyToClipboard() {
    var copyText = document.getElementById("full-text");
    
    var tempTextArea = document.createElement("textarea");
    tempTextArea.value = copyText.innerText;
    
    document.body.appendChild(tempTextArea);
    
    tempTextArea.select();
    tempTextArea.setSelectionRange(0, 99999);
    
    try {
        var successful = document.execCommand('copy');
        var msg = successful ? "התוצאה הועתקה ללוח!" : "ההעתקה נכשלה, אנא נסה שוב.";
        alert(msg);
    } catch (err) {
        console.error('שגיאה בהעתקה:', err);
        alert('אירעה שגיאה בהעתקה. אנא נסה להעתיק ידנית.');
    }
    
    document.body.removeChild(tempTextArea);
}
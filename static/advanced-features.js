// ניהול היסטוריית קישורים
class LinkHistory {
    constructor() {
        this.history = JSON.parse(localStorage.getItem('linkHistory') || '[]');
    }

    addLink(linkData) {
        this.history.unshift({
            ...linkData,
            timestamp: new Date().toISOString()
        });
        this.history = this.history.slice(0, 50); // שמירת 50 קישורים אחרונים
        localStorage.setItem('linkHistory', JSON.stringify(this.history));
    }

    getHistory() {
        return this.history;
    }
}

// ניהול תצוגה מקדימה מתקדמת
class AdvancedPreview {
    static async generatePreview(linkData) {
        try {
            const response = await fetch('/api/preview', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(linkData)
            });
            return await response.json();
        } catch (error) {
            console.error('Preview generation failed:', error);
            throw error;
        }
    }
}

// Analytics tracking
class Analytics {
    static trackLinkGeneration(linkData) {
        // Implementation for analytics tracking
        console.log('Link generated:', linkData);
    }
}

// הוספת class לניהול תזמונים
class ScheduleManager {
    static async scheduleLink(linkData) {
        try {
            const response = await fetch('/schedule_link', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(linkData)
            });
            
            const result = await response.json();
            if (result.error) {
                throw new Error(result.error);
            }
            
            return result;
        } catch (error) {
            console.error('Scheduling failed:', error);
            throw error;
        }
    }

    static formatScheduleTime(dateTimeLocal) {
        // המרת התאריך לפורמט ISO
        return new Date(dateTimeLocal).toISOString();
    }
}

// עדכון הפונקציה generateLink
function generateLink(isPreview = false) {
    const baseLink = $('#baseLink').val();
    const agentId = $('#agent').val();
    const freeText = $('#freeText').val();
    const scheduleTime = $('#scheduleTime').val();
    const utmSource = $('#utmSource').val();
    const utmMedium = $('#utmMedium').val();
    
    if (scheduleTime) {
        // אם נבחר זמן תזמון, נשלח לתזמון
        const linkData = {
            link: baseLink,
            agent_id: agentId,
            free_text: freeText,
            schedule_time: ScheduleManager.formatScheduleTime(scheduleTime),
            utm_source: utmSource,
            utm_medium: utmMedium
        };
        
        ScheduleManager.scheduleLink(linkData)
            .then(result => {
                alert(`הקישור תוזמן בהצלחה לתאריך: ${new Date(result.scheduled_time).toLocaleString()}`);
            })
            .catch(error => {
                alert('אירעה שגיאה בתזמון הקישור: ' + error.message);
            });
    } else {
        // אם לא נבחר זמן, נמשיך כרגיל
        // ... הקוד הקיים ...
    }
}

// ניהול סוכנים
class AgentManager {
    static async addAgent(agentData) {
        try {
            const response = await fetch('/api/agents', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(agentData)
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to add agent');
            }
            
            const result = await response.json();
            
            // רענון הדף לאחר הוספה מוצלחת
            window.location.reload();
            return result;
        } catch (error) {
            console.error('Failed to add agent:', error);
            throw error;
        }
    }
}

// הוספת מאזיני אירועים למודל הוספת סוכן
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('agentModal');
    const openModalBtn = document.getElementById('openAgentModal');
    const closeModalBtn = document.getElementById('closeAgentModal');
    const addAgentForm = document.getElementById('addAgentForm');
    const agentSelect = document.getElementById('agent');

    if (openModalBtn) {
        openModalBtn.addEventListener('click', () => {
            modal.classList.remove('hidden');
            document.getElementById('agentFullName').focus();
        });
    }

    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', () => {
            modal.classList.add('hidden');
            addAgentForm.reset();
        });
    }

    if (addAgentForm) {
        addAgentForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const fullName = document.getElementById('agentFullName').value.trim();
            const referralId = document.getElementById('agentReferralId').value.trim();
            
            // בדיקות תקינות
            if (!fullName) {
                alert('נא להזין שם סוכן');
                return;
            }
            if (!/^\d{4}$/.test(referralId)) {
                alert('מספר מפנה חייב להכיל 4 ספרות בדיוק');
                return;
            }

            try {
                const response = await fetch('/api/agents', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        first_name: fullName,
                        last_name: '',  // שם משפחה ריק כי אנחנו מקבלים שם מלא
                        referral_id: referralId
                    })
                });

                if (!response.ok) {
                    throw new Error('שגיאה בהוספת הסוכן');
                }

                // הוספת הסוכן החדש לרשימה הנפתחת
                const option = document.createElement('option');
                option.value = referralId;
                option.text = `${fullName} (${referralId})`;
                agentSelect.add(option);
                agentSelect.value = referralId;  // בחירת הסוכן החדש

                modal.classList.add('hidden');
                addAgentForm.reset();
                alert('הסוכן נוסף בהצלחה!');
            } catch (error) {
                alert(error.message);
            }
        });
    }

    // סגירת המודל בלחיצה מחוץ לו
    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.add('hidden');
            addAgentForm.reset();
        }
    });

    // מניעת הזנת תווים שאינם ספרות במספר מפנה
    const referralIdInput = document.getElementById('agentReferralId');
    if (referralIdInput) {
        referralIdInput.addEventListener('input', function() {
            this.value = this.value.replace(/[^0-9]/g, '').slice(0, 4);
        });
    }
});

// הוספת קוד לטיפול בשדות הטופס
document.querySelectorAll('#addAgentForm input').forEach(input => {
    input.addEventListener('input', function() {
        this.classList.remove('border-red-500');
    });
});

// תבניות מסרים חכמות
const smartTemplates = {
    urgency: {
        generate: (title) => `⏰ הזדמנות מוגבלת בזמן!
${title}
הצטרפו עכשיו לפני שייגמר המלאי 🔥`,
    },
    'social-proof': {
        generate: (title) => `👥 מאות אנשים כבר הצטרפו!
${title}
בואו להיות חלק מהקהילה המצליחה שלנו 🌟`,
    },
    fomo: {
        generate: (title) => `🎯 אל תפספסו!
${title}
הצטרפו עכשיו והבטיחו את מקומכם 💫`,
    },
    benefit: {
        generate: (title) => `✨ הזדמנות מיוחדת עבורכם!
${title}
הצטרפו וקבלו את כל היתרונות המיוחדים 🎁`,
    }
};

// הוספת מאזיני אירועים לתבניות החכמות
document.addEventListener('DOMContentLoaded', function() {
    const freeTextArea = document.getElementById('freeText');
    
    document.querySelectorAll('.smart-template').forEach(button => {
        button.addEventListener('click', function() {
            const templateType = this.dataset.template;
            const title = document.getElementById('preview-title')?.textContent || 'הזדמנות חדשה';
            
            if (smartTemplates[templateType]) {
                freeTextArea.value = smartTemplates[templateType].generate(title);
            }
        });
    });

    // הוספת מאזיני אירועים לתבניות הרגילות
    document.querySelectorAll('.message-template').forEach(button => {
        button.addEventListener('click', function() {
            freeTextArea.value = this.dataset.message;
        });
    });
});

// שמירת היסטוריית קישורים
const linkHistory = {
    add(linkData) {
        let history = JSON.parse(localStorage.getItem('linkHistory') || '[]');
        history.unshift({
            ...linkData,
            timestamp: new Date().toISOString()
        });
        history = history.slice(0, 50); // שמירת 50 קישורים אחרונים
        localStorage.setItem('linkHistory', JSON.stringify(history));
    },

    get() {
        return JSON.parse(localStorage.getItem('linkHistory') || '[]');
    }
};

// הוספת הקישור להיסטוריה בעת יצירה
$(document).ready(function() {
    const originalGenerateLink = window.generateLink;
    window.generateLink = function(isPreview = false) {
        originalGenerateLink(isPreview);
        
        if (!isPreview) {
            linkHistory.add({
                baseLink: $('#baseLink').val(),
                agentId: $('#agent').val(),
                freeText: $('#freeText').val()
            });
        }
    };
});

// הוספת פונקציה לטעינת נתונים מהשרת
async function loadSavedLinksFromServer() {
    try {
        const agentId = document.getElementById('agent').value;
        const response = await fetch(`/api/saved-links/${agentId}`);
        const savedLinks = await response.json();
        
        // שמירה ב-localStorage
        localStorage.setItem('savedLinks', JSON.stringify(savedLinks));
        
        // הצגת הקישורים
        displaySavedLinks();
    } catch (error) {
        console.error('Error loading saved links:', error);
    }
}

// הוספת פונקציה לשמירת קישור בשרת
async function saveLinkToServer(linkData) {
    try {
        const response = await fetch(`/api/saved-links/${linkData.agentId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(linkData)
        });
        
        if (!response.ok) {
            throw new Error('Failed to save link');
        }
        
        // טעינה מחדש של הקישורים מהשרת
        await loadSavedLinksFromServer();
    } catch (error) {
        console.error('Error saving link:', error);
        alert('שגיאה בשמירת הקישור');
    }
}

// עדכון פונקציית saveLink
function saveLink() {
    const title = document.getElementById('savedLinkTitle').value.trim();
    const text = document.getElementById('savedLinkText').value.trim();
    const postText = document.getElementById('savedPostText').value.trim();
    const agentId = document.getElementById('agent').value;
    
    if (!title || !text) {
        alert('נא למלא את כל השדות הנדרשים');
        return;
    }
    
    // שמירה בשרת
    saveLinkToServer({
        title,
        text,
        postText,
        agentId
    });
}

// טעינת הקישורים בטעינת הדף ובשינוי סוכן
document.addEventListener('DOMContentLoaded', loadSavedLinksFromServer);
document.getElementById('agent').addEventListener('change', loadSavedLinksFromServer); 
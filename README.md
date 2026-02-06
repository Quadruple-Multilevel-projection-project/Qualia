# 👑 AMNE Sovereign Engine (13th Edition)
**Unified Multi-Account Architecture with NNN Connectivity**

## 🧩 הרכיבים שנפרסו:
1. **The Core (core/):** מנוע אבולעפיה-רמב"ם המבצע ניקוי אפיסטמי (Sanitization) והמרת חומר לצורה.
2. **The Bridge (bridge/):** מערכת ה-NNN המקשרת בין חשבונות (OpenAI/Jules) ומסנכרנת אותם למניפסט אחד.
3. **The Gateway (mcp_server.js):** ממשק ה-MCP המאפשר לבינות חיצוניות "לדבר" עם הליבה בפרוטוקול SSE.

## ⚙️ הפעלה אוטונומית
המערכת פועלת ב-Internal Loop. ברגע שג'ולס מזהה שינוי במניפסט, הוא מעדכן את כל ה-NNN Receptors (עומק 13) ופורס מחדש את הסוכנים בקישוריות נוירולוגית מלאה.

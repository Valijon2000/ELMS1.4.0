# Render.com ga Deploy qilish

## Qadamlar

### 1. GitHub'ga kod yuklash
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo-url>
git push -u origin main
```

### 2. Render.com'da yangi Web Service yaratish

1. [Render.com](https://render.com) ga kiring
2. "New +" tugmasini bosing
3. "Web Service" ni tanlang
4. GitHub repository'ni ulang
5. Quyidagi sozlamalarni kiriting:
   - **Name**: elms (yoki istalgan nom)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn run:app`
   - **Plan**: Free (yoki istalgan plan)

### 3. Environment Variables qo'shish

Render Dashboard'da "Environment" bo'limiga quyidagilarni qo'shing:

- **SECRET_KEY**: Tasodifiy kalit (yoki Render avtomatik yaratadi)
- **DATABASE_URL**: PostgreSQL database connection string (Render avtomatik yaratadi)
- **FLASK_DEBUG**: `False` (production uchun)

### 4. PostgreSQL Database yaratish

1. Render Dashboard'da "New +" → "PostgreSQL" ni tanlang
2. Database nomini kiriting: `elms-db`
3. Plan: Free (yoki istalgan plan)
4. Database yaratilgandan keyin, connection string avtomatik `DATABASE_URL` environment variable sifatida Web Service'ga qo'shiladi

### 5. Database Migration

Ilovani birinchi marta ishga tushirganda, database jadvalari avtomatik yaratiladi (`db.create_all()` funksiyasi orqali).

Agar migration kerak bo'lsa:
```bash
# Local'da
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. File Uploads

**Muhim**: Render'da file system ephemeral (vaqtinchalik) bo'ladi. Fayllar server qayta ishga tushganda yo'qoladi.

**Yechimlar**:
1. **Render Disk** (paid plan) - Persistent storage
2. **AWS S3** yoki boshqa cloud storage
3. **Database'ga saqlash** (kichik fayllar uchun)

Hozircha, fayllar vaqtinchalik saqlanadi. Production uchun cloud storage integratsiya qilish tavsiya etiladi.

### 7. Custom Domain (ixtiyoriy)

1. Render Dashboard'da Web Service'ni oching
2. "Settings" → "Custom Domains"
3. Domen nomini qo'shing
4. DNS sozlamalarini kiriting

## Troubleshooting

### Database connection xatosi
- `DATABASE_URL` to'g'ri sozlanganligini tekshiring
- PostgreSQL database ishlayotganligini tekshiring

### Build xatosi
- `requirements.txt` da barcha kutubxonalar borligini tekshiring
- Python versiyasi to'g'ri ekanligini tekshiring (`.runtime.txt`)

### Application xatosi
- Render Logs'ni tekshiring
- Environment variables to'g'ri ekanligini tekshiring

## Production sozlamalari

- `DEBUG = False` bo'lishi kerak
- `SECRET_KEY` kuchli bo'lishi kerak
- HTTPS avtomatik yoqiladi (Render'da)
- Static files Flask orqali serve qilinadi

## Monitoring

Render Dashboard'da quyidagilarni kuzatishingiz mumkin:
- Logs
- Metrics (CPU, Memory, Requests)
- Events


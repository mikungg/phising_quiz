from flask import Flask, redirect, url_for, send_from_directory, jsonify, session, request
import random

app = Flask(__name__)

app.secret_key = "your-secret-key-here-change-in-production"

@app.route('/')
def home():
    return redirect(url_for('id_page'))

@app.route('/id')
def id_page():
    return send_from_directory('id', 'index.html')

@app.route('/id/quiz')
def id_quiz():
    return send_from_directory('id', 'quiz.html')

@app.route('/en')
def en_page():
    return send_from_directory('en', 'index.html')

@app.route('/en/quiz')
def en_quiz():
    return send_from_directory('en', 'quiz.html')

@app.route('/api/quiz-data/<lang>')
def get_quiz_data(lang='id'):
    if lang not in ['id', 'en']:
        return jsonify({'error': 'Invalid language'}), 400
    
    if lang == 'id':
        # Quiz data array for Indonesian
        quiz_data = [
                {
                    "judul": "Contoh Email",
                    "deskripsi": "Email meminta Anda untuk melakukan review pada dokumen yang tidak jelas.",
                    "soalHtml": "../static/iframe-soal-id/phishing1.html",
                    "penjelasan": "Perhatikan link saat anda mengarahkan kursor diatas link dan lihat ke sebelah kiri bawah layar. Link tersebut bukan domain resmi dan meminta kredensial — ini ciri phishing."
            },
            {
                "judul": "Contoh Email",
                "deskripsi": "Email perangkat baru masuk.",
                "soalHtml": "../static/iframe-soal-id/phishing2.html",
                "penjelasan": "Perhatikan link saat anda mengarahkan kursor diatas link dan lihat ke sebelah kiri bawah layar. \"google.real.support\" merupakan subdomain dari \"real.support\" yang bukan merupakan domain resmi Google — ini ciri phishing."
            },
            {
                "judul": "Contoh Email",
                "deskripsi": "Email mengklaim 'Seseorang mengetahui kata sandi Anda' dengan tombol 'GANTI KATA SANDI'.",
                "soalHtml": "../static/iframe-soal-id/phishing3.html",
                "penjelasan": "Perhatikan link saat anda mengarahkan kursor diatas link dan lihat ke sebelah kiri bawah layar. Pengirim memakai alamat yang bukan domain resmi Google (contoh: no-reply@google.support.org) dan tombol mengarah ke domain asing (contoh: xyzsecurityxyz.org) namun memiliki subdomain yang menyerupai Google (contoh: myaccount.google.com-securitysettingpage.xyzsecurityxyz.org). Jangan klik tautan — ini ciri phishing."
            },
            {
                "judul": "Contoh Email",
                "deskripsi": "Email mengaku dari Dropbox dengan tombol 'LIHAT FOLDER' mungkin ini file penting?",
                "soalHtml": "../static/iframe-soal-id/phishing4.html",
                "penjelasan": "Perhatikan link saat anda mengarahkan kursor diatas link dan lihat ke sebelah kiri bawah layar. Pengirim memakai domain yang menyerupai Dropbox (contoh: `dropbox-online.net`) tetapi bukan domain resmi `dropbox.com`. Tautan 'LIHAT FOLDER' mengarah ke domain asing (contoh: dropbox-online.net/importantfolder) yang bisa digunakan untuk mencuri kredensial atau menyebarkan malware. Jangan klik tautan; buka `dropbox.com` langsung dan periksa undangan di akun Anda — ini ciri phishing."
            },
            {
                "judul": "Contoh Email",
                "deskripsi": "Email mengklaim 'Pemberitahuan Penghentian' dari Help Desk yang mendesak pembatalan atau meminta Anda menghubungi nomor dukungan.",
                "soalHtml": "../static/iframe-soal-id/phishing5.html",
                "penjelasan": "Pesan membuat rasa urgensi (akun akan dihentikan) dan meminta Anda menghubungi nomor atau melakukan tindakan segera, taktik umum social engineering. Alamat pengirim bisa dipalsukan (helpdesk@itss.co.id), dan nomor telepon/tautan yang diberikan dapat digunakan untuk meminta kredensial atau pembayaran. Jangan menghubungi nomor atau memberikan informasi. Verifikasi langsung ke helpdesk resmi melalui saluran yang Anda kenal (contoh: portal perusahaan atau nomor internal) — ini ciri phishing."
            },
            {
                "judul": "Contoh Pesan SMS",
                "deskripsi": "SMS mengaku dari Netflix tentang akun ditangguhkan dan menyertakan tautan pemulihan — periksa pengirim dan URL sebelum mengklik.",
                "soalHtml": "../static/iframe-soal-id/phishing6.html",
                "penjelasan": "Pengirim menggunakan alamat/identitas yang bukan milik Netflix (contoh: netflix@mnasdfkjasdf.org) dan tautan pemulihan memakai domain yang menipu (contoh: `www.netflix.com.onlinehome.id`) yang hanya menyerupai Netflix tetapi sebenarnya berada di domain lain (onlinehome.id). Tautan seperti ini sering dipakai untuk mencuri kredensial atau memasang malware. Jangan klik tautan; buka `netflix.com` langsung atau periksa status pembayaran dari aplikasi resmi — ini ciri phishing."
            },
            {
                "judul": "Contoh Pesan SMS",
                "deskripsi": "Tiba- tiba ada yang SMS mengaku Anda pemenang undian (mis. 'Pemenang Ke-2 Shopee') dan menyertakan link pendek (bit.ly) untuk klaim hadiah. Keberuntungan?",
                "soalHtml": "../static/iframe-soal-id/phishing7.html",
                "penjelasan": "Pesan mengklaim Anda pemenang dan memaksa tindakan cepat serta menyertakan link pendek (contoh: bit.ly/pemenangundian2) yang menyembunyikan tujuan sebenarnya. Pengirim berasal dari nomor tidak dikenal dan klaim hadiah yang tidak Anda tunggu adalah tanda umum penipuan — ini ciri phishing."
            },
            {
                "judul": "Contoh Pesan WhatsApp",
                "deskripsi": "Pesan WhatsApp berisi lampiran .apk berjudul 'Surat Undangan Pernikahan Digital'.",
                "soalHtml": "../static/iframe-soal-id/phishing8.html",
                "penjelasan": "Berbahaya. Lampiran berformat .apk adalah paket aplikasi Android yang dapat mengandung malware. Menerima .apk lewat WhatsApp dari nomor tidak dikenal adalah tanda penipuan/malware — ini ciri phishing."
            },
            {
                "judul": "Contoh Pesan WhatsApp",
                "deskripsi": "Pesan mengaku dari instansi KEMENDIKBUD menawarkan kuota/pulsa dengan tautan domain tidak resmi.",
                "soalHtml": "../static/iframe-soal-id/phishing9.html",
                "penjelasan": "Penipu sering memalsukan nama instansi resmi dan menggunakan domain atau tautan yang mirip (contoh: `subsidi-kuota.online` atau tautan singkat) untuk mengelabui penerima. Tanda-tanda: pengirim nomor tidak dikenal, tautan bukan domain resmi pemerintah, serta batas waktu mendesak — ini ciri phishing."
            },
            {
                "judul": "Contoh Email",
                "deskripsi": "Pemberitahuan keamanan LinkedIn tentang percobaan masuk dari perangkat baru.",
                "soalHtml": "../static/iframe-soal-id/legit1.html",
                "penjelasan": "Email ini tampak sah karena berasal dari domain resmi (`security-noreply@linkedin.com`) dan menampilkan merek/branding LinkedIn yang konsisten. Isi berisi salam personal, metadata kontekstual (tanggal, browser/perangkat), dan tautan ke Pusat Bantuan — pola yang umum pada pemberitahuan keamanan asli. Selain itu, pesan tidak meminta kredensial secara langsung atau menekan Anda untuk segera memasukkan kata sandi melalui tautan pihak ketiga."
            },
            {
                "judul": "Contoh Email",
                "deskripsi": "Newsletter Letterboxd ('Rushes') dengan header bergambar.",
                "soalHtml": "../static/iframe-soal-id/legit2.html",
                "penjelasan": "Email ini tampak sah karena menggunakan pengirim dari domain Letterboxd (`robot@letterboxd.com`) dan menampilkan branding/header yang konsisten. Tautan CTA mengarah ke `letterboxd.com` dengan parameter UTM (bukan domain asing), isi bersifat informatif (digest/summary) dan tidak meminta kredensial atau tindakan berisiko. Cara cepat memverifikasi: arahkan kursor ke tautan untuk memastikan domain adalah `letterboxd.com`, atau buka `letterboxd.com` langsung jika ragu."
            },
            {
                "judul": "Contoh Email Ad",
                "deskripsi": "Iklan bersponsor dari Android Developers yang menampilkan gambar produk dan tombol 'Learn more'.",
                "soalHtml": "../static/iframe-soal-id/legit3.html",
                "penjelasan": "Ini tampak sah sebagai iklan resmi karena menampilkan branding Android/Google yang konsisten dan tautan yang diarahkan melalui layanan iklan resmi (contoh: `googleadservices.com`) menuju halaman pengiklan. Anda juga bisa memverifikasi dengan mengunjungi situs resmi Android Developers (developer.android.com)."
            },
            {
                "judul": "Contoh Email",
                "deskripsi": "Pemberitahuan keamanan Goodreads tentang percobaan masuk ke akun Anda.",
                "soalHtml": "../static/iframe-soal-id/legit4.html",
                "penjelasan": "Email ini terlihat sah: pengirim menggunakan domain resmi (`account-update@goodreads.com`), pesan menyertakan metadata kontekstual (tanggal/waktu, perangkat, lokasi), serta tidak meminta kredensial lewat tautan pihak ketiga. Untuk memverifikasi, arahkan kursor ke tautan untuk memastikan domain adalah `goodreads.com` atau buka `goodreads.com` langsung."
            },
            {
                "judul": "Contoh Email",
                "deskripsi": "Pemberitahuan keamanan X (Twitter) tentang percobaan masuk dari perangkat baru.",
                "soalHtml": "../static/iframe-soal-id/legit5.html",
                "penjelasan": "Email ini terlihat asli karena dikirim dari domain resmi (`verify@x.com`), dan menyertakan informasi konteks (lokasi, perangkat, waktu) serta tautan tindakan resmi (mis. ubah kata sandi, tinjau aplikasi). Pesan tidak meminta kredensial lewat formulir pihak ketiga dan berisi tautan bantuan/dukungan resmi. Cara memverifikasi: arahkan kursor ke tautan untuk memastikan tujuan adalah `x.com` atau buka `x.com` langsung melalui browser."
            },
            {
                "judul": "Contoh Pesan SMS",
                "deskripsi": "SMS promosi dari myIM3 yang menawarkan fitur SATSPAM.",
                "soalHtml": "../static/iframe-soal-id/legit6.html",
                "penjelasan": "Tampak sah: pengirim menyebut 'myIM3' dan tautan menggunakan domain pendek `myim3.co` yang kemungkinan merupakan layanan resmi operator. Cara verifikasi: periksa ID pengirim/nomor apakah mirip dengan nomor layanan operator, jangan langsung memasukkan informasi lewat tautan; buka aplikasi resmi myIM3 atau kunjungi situs operator yang Anda kenal untuk mengaktifkan fitur, atau hubungi layanan pelanggan jika ragu. Hati-hati jika tautan meminta kredensial atau pembayaran di luar kanal resmi."
            },
            {
                "judul": "Contoh Pesan SMS",
                "deskripsi": "SMS dari McDonald's berisi promosi PaNas dengan tautan ke sda-ida.id.",
                "soalHtml": "../static/iframe-soal-id/legit7.html",
                "penjelasan": "Tampak sah: pesan ini berasal dari kampanye promosi resmi McDonald's Indonesia. Domain `sda-ida.id` adalah layanan URL yang berkaitan dengan Indosat Digital Analytics (iDA) dari Indosat Ooredoo. Cara verifikasi: cek apakah pengirim adalah nomor yang dikenal dari McDonald's (sering muncul sebagai 'McDonald's' di ID pengirim), periksa konsistensi branding (nama aplikasi, gaya bahasa promosi khas McD), dan pastikan tautan pendek mengarah ke domain resmi McDonald's atau aplikasi mereka. Meski legitimate, tetap berhati-hati dengan tautan pendek."
            },
            {
                "judul": "Contoh Pesan WhatsApp",
                "deskripsi": "Pesan WhatsApp dari akun terverifikasi dengan tanda centang hijau, menawarkan promosi belanja.",
                "soalHtml": "../static/iframe-soal-id/legit8.html",
                "penjelasan": "Tampak sah: pesan ini berasal dari akun WhatsApp Business resmi yang terverifikasi (ditandai dengan centang hijau ✓ di samping nama pengirim). Tanda verifikasi hijau adalah fitur resmi WhatsApp yang hanya diberikan kepada akun bisnis yang telah diverifikasi identitasnya oleh WhatsApp. Pesan berisi promosi belanja dengan personalisasi nama penerima, gaya bahasa marketing yang konsisten dengan brand Cara verifikasi: pastikan ada centang hijau verifikasi di nama pengirim, periksa apakah nama akun cocok dengan brand resmi, cek riwayat chat sebelumnya dengan nomor yang sama, dan jika ada tautan, pastikan mengarah ke domain resmi perusahaan. Meski legitimate, tetap berhati-hati — jangan langsung klik tautan tanpa memverifikasi tujuan URL."
            },
            {
                "judul": "Contoh Pesan WhatsApp",
                "deskripsi": "Pesan WhatsApp dari akun terverifikasi dengan tanda centang hijau, menawarkan promosi berlangganan.",
                "soalHtml": "../static/iframe-soal-id/legit9.html",
                "penjelasan": "Tampak sah: pesan ini berasal dari akun WhatsApp Business resmi yang terverifikasi (ditandai dengan centang hijau ✓ di samping nama pengirim 'Gojek Indonesia'). Tanda verifikasi hijau adalah fitur resmi WhatsApp yang hanya diberikan kepada akun bisnis yang telah diverifikasi identitasnya oleh WhatsApp. Pesan berisi promosi re-subscription Gojek PLUS dengan personalisasi nama penerima ('John Doe, gak usah gengsi...😉'), menyebutkan benefit spesifik layanan (diskon GoFood, GoRide, GoCar, GoMart s.d. 10rb/8rb), dan menggunakan gaya bahasa marketing informal yang konsisten dengan brand Gojek. Cara verifikasi: pastikan ada centang hijau verifikasi di nama pengirim, periksa apakah nama akun cocok dengan brand resmi ('Gojek Indonesia'), cek riwayat chat sebelumnya dengan nomor yang sama untuk melihat pesan-pesan sebelumnya dari Gojek, dan jika ada tautan, verifikasi mengarah ke domain resmi atau dalam aplikasi. Meski legitimate, tetap berhati-hati."
            }
        ]
    elif lang == 'en':
        # Quiz data array for English
        quiz_data = [
            {
                "judul": "Email Example",
                "deskripsi": "Email asking you to review an unclear document.",
                "soalHtml": "../static/iframe-soal-en/phishing1.html",
                "penjelasan": "Notice the link when you hover your cursor over it and look at the bottom left of the screen. The link is not an official domain and requests credentials — this is a phishing characteristic."
            },
            {
                "judul": "Email Example",
                "deskripsi": "Email about new device login.",
                "soalHtml": "../static/iframe-soal-en/phishing2.html",
                "penjelasan": "Notice the link when you hover your cursor over it and look at the bottom left of the screen. \"google.real.support\" is a subdomain of \"real.support\" which is not an official Google domain — this is a phishing characteristic."
            },
            {
                "judul": "Email Example",
                "deskripsi": "Email claiming 'Someone knows your password' with a 'CHANGE PASSWORD' button.",
                "soalHtml": "../static/iframe-soal-en/phishing3.html",
                "penjelasan": "Notice the link when you hover your cursor over it and look at the bottom left of the screen. The sender uses an address that is not an official Google domain (example: no-reply@google.support.org) and the button points to a foreign domain (example: xyzsecurityxyz.org) but has a subdomain resembling Google (example: myaccount.google.com-securitysettingpage.xyzsecurityxyz.org). Don't click the link — this is a phishing characteristic."
            },
            {
                "judul": "Email Example",
                "deskripsi": "Email claiming to be from Dropbox with a 'VIEW FOLDER' button - could this be an important file?",
                "soalHtml": "../static/iframe-soal-en/phishing4.html",
                "penjelasan": "Notice the link when you hover your cursor over it and look at the bottom left of the screen. The sender uses a domain resembling Dropbox (example: `dropbox-online.net`) but not the official `dropbox.com` domain. The 'VIEW FOLDER' link points to a foreign domain (example: dropbox-online.net/importantfolder) that could be used to steal credentials or spread malware. Don't click the link; go directly to `dropbox.com` and check invitations in your account — this is a phishing characteristic."
            },
            {
                "judul": "Email Example",
                "deskripsi": "Email claiming 'Suspension Notice' from Help Desk urging cancellation or asking you to contact support number.",
                "soalHtml": "../static/iframe-soal-en/phishing5.html",
                "penjelasan": "The message creates urgency (account will be suspended) and asks you to call a number or take immediate action, a common social engineering tactic. The sender's address can be forged (helpdesk@itss.co.id), and the phone number/link provided can be used to request credentials or payment. Don't call the number or provide information. Verify directly with the official helpdesk through channels you know (example: company portal or internal number) — this is a phishing characteristic."
            },
            {
                "judul": "SMS Example",
                "deskripsi": "SMS claiming to be from Netflix about suspended account with recovery link — check sender and URL before clicking.",
                "soalHtml": "../static/iframe-soal-en/phishing6.html",
                "penjelasan": "The sender uses an address/identity not belonging to Netflix (example: netflix@mnasdfkjasdf.org) and the recovery link uses a deceptive domain (example: `www.netflix.com.onlinehome.id`) that only resembles Netflix but is actually on another domain (onlinehome.id). Links like this are often used to steal credentials or install malware. Don't click the link; go directly to `netflix.com` or check payment status from the official app — this is a phishing characteristic."
            },
            {
                "judul": "SMS Example",
                "deskripsi": "Suddenly receiving SMS claiming you won a lottery (e.g., 'Shopee Winner #2') with a short link (bit.ly) to claim prize. Lucky day?",
                "soalHtml": "../static/iframe-soal-en/phishing7.html",
                "penjelasan": "The message claims you're a winner and forces quick action while including a short link (example: bit.ly/pemenangundian2) that hides the real destination. The sender is from an unknown number and unexpected prize claims are common signs of fraud — this is a phishing characteristic."
            },
            {
                "judul": "WhatsApp Example",
                "deskripsi": "WhatsApp message containing .apk attachment titled 'Digital Wedding Invitation'.",
                "soalHtml": "../static/iframe-soal-en/phishing8.html",
                "penjelasan": "Dangerous. Attachments in .apk format are Android application packages that can contain malware. Receiving .apk via WhatsApp from unknown numbers is a sign of fraud/malware — this is a phishing characteristic."
            },
            {
                "judul": "WhatsApp Example",
                "deskripsi": "Message claiming to be from KEMENDIKBUD institution offering data/credit quota with unofficial domain link.",
                "soalHtml": "../static/iframe-soal-en/phishing9.html",
                "penjelasan": "Scammers often impersonate official institutions and use similar domains or links (example: `subsidi-kuota.online` or short links) to deceive recipients. Signs: sender from unknown number, link is not official government domain, and urgent deadline — this is a phishing characteristic."
            },
            {
                "judul": "Email Example",
                "deskripsi": "LinkedIn security notification about login attempt from new device.",
                "soalHtml": "../static/iframe-soal-en/legit1.html",
                "penjelasan": "This email appears legitimate because it comes from an official domain (`security-noreply@linkedin.com`) and displays consistent LinkedIn branding. The content includes a personal greeting, contextual metadata (date, browser/device), and links to Help Center — patterns common in genuine security notifications. Additionally, the message does not directly request credentials or pressure you to immediately enter a password through a third-party link."
            },
            {
                "judul": "Email Example",
                "deskripsi": "Letterboxd newsletter ('Rushes') with illustrated header.",
                "soalHtml": "../static/iframe-soal-en/legit2.html",
                "penjelasan": "This email appears legitimate because it uses a sender from the Letterboxd domain (`robot@letterboxd.com`) and displays consistent branding/header. CTA links point to `letterboxd.com` with UTM parameters (not foreign domains), the content is informative (digest/summary) and does not request credentials or risky actions. Quick verification: hover cursor over links to ensure the domain is `letterboxd.com`, or go directly to `letterboxd.com` if in doubt."
            },
            {
                "judul": "Email Ad Example",
                "deskripsi": "Sponsored ad from Android Developers showing product image and 'Learn more' button.",
                "soalHtml": "../static/iframe-soal-en/legit3.html",
                "penjelasan": "This appears legitimate as an official ad because it displays consistent Android/Google branding and links directed through official ad services (example: `googleadservices.com`) to the advertiser's page. You can also verify by visiting the official Android Developers site (developer.android.com)."
            },
            {
                "judul": "Email Example",
                "deskripsi": "Goodreads security notification about login attempt to your account.",
                "soalHtml": "../static/iframe-soal-en/legit4.html",
                "penjelasan": "This email appears legitimate: the sender uses an official domain (`account-update@goodreads.com`), the message includes contextual metadata (date/time, device, location), and does not request credentials through third-party links. To verify, hover cursor over links to ensure the domain is `goodreads.com` or go directly to `goodreads.com`."
            },
            {
                "judul": "Email Example",
                "deskripsi": "X (Twitter) security notification about login attempt from new device.",
                "soalHtml": "../static/iframe-soal-en/legit5.html",
                "penjelasan": "This email appears genuine because it's sent from an official domain (`verify@x.com`), and includes contextual information (location, device, time) as well as official action links (e.g., change password, review apps). The message does not request credentials through third-party forms and contains official help/support links. Verification method: hover cursor over links to ensure destination is `x.com` or go directly to `x.com` via browser."
            },
            {
                "judul": "SMS Example",
                "deskripsi": "Promotional SMS from myIM3 offering SATSPAM feature.",
                "soalHtml": "../static/iframe-soal-en/legit6.html",
                "penjelasan": "Appears legitimate: sender mentions 'myIM3' and link uses short domain `myim3.co` which is likely an official operator service. Verification method: check sender ID/number if it matches operator service numbers, don't immediately enter information through links; open official myIM3 app or visit the operator site you know to activate features, or contact customer service if in doubt. Be careful if link requests credentials or payment outside official channels."
            },
            {
                "judul": "SMS Example",
                "deskripsi": "SMS from McDonald's containing PaNas promotion with link to sda-ida.id.",
                "soalHtml": "../static/iframe-soal-en/legit7.html",
                "penjelasan": "Appears legitimate: this message comes from an official McDonald's Indonesia promotional campaign. The domain `sda-ida.id` is a URL service related to Indosat Digital Analytics (iDA) from Indosat Ooredoo. Verification method: check if sender is a known McDonald's number (often appears as 'McDonald's' in sender ID), verify branding consistency (app name, typical McD promotional language style), and ensure short link points to official McDonald's domain or their app. Even though legitimate, remain cautious with short links."
            },
            {
                "judul": "WhatsApp Example",
                "deskripsi": "WhatsApp message from verified account with green checkmark, offering shopping promotion.",
                "soalHtml": "../static/iframe-soal-en/legit8.html",
                "penjelasan": "Appears legitimate: this message comes from an official verified WhatsApp Business account (marked with green checkmark ✓ next to sender name). The green verification badge is an official WhatsApp feature only given to business accounts whose identity has been verified by WhatsApp. The message contains shopping promotion with recipient name personalization, marketing language style consistent with the brand. Verification method: ensure there's a green verification checkmark on sender name, check if account name matches official brand, review previous chat history with the same number, and if there are links, ensure they point to the company's official domain. Even though legitimate, remain cautious — don't immediately click links without verifying URL destination."
            },
            {
                "judul": "WhatsApp Example",
                "deskripsi": "WhatsApp message from verified account with green checkmark, offering subscription promotion.",
                "soalHtml": "../static/iframe-soal-en/legit9.html",
                "penjelasan": "Appears legitimate: this message comes from an official verified WhatsApp Business account (marked with green checkmark ✓ next to sender name 'Gojek Indonesia'). The green verification badge is an official WhatsApp feature only given to business accounts whose identity has been verified by WhatsApp. The message contains Gojek PLUS re-subscription promotion with recipient name personalization ('John Doe, gak usah gengsi...😉'), mentions specific service benefits (GoFood, GoRide, GoCar, GoMart discounts up to 10k/8k), and uses informal marketing language style consistent with Gojek brand. Verification method: ensure there's a green verification checkmark on sender name, check if account name matches official brand ('Gojek Indonesia'), review previous chat history with the same number to see previous Gojek messages, and if there are links, verify they point to official domain or in-app. Even though legitimate, remain cautious."
            }
        ]

    # Shuffle the quiz data
    shuffled = quiz_data.copy()
    random.shuffle(shuffled)
    
    # Store in session for consistency during the quiz
    session['quiz_data'] = shuffled
    
    return jsonify(shuffled)

@app.route('/api/check-answer/<lang>', methods=['POST'])
def check_answer(lang='id'):
    if lang not in ['id', 'en']:
        return jsonify({'error': 'Invalid language'}), 400

    data = request.get_json()
    soal_html = data.get('soalHtml')
    user_answer = data.get('answer')
    
    # Find the question in quiz_data by matching soalHtml
    question = None

    if lang == 'id':
        for q in quiz_data:
            if q['soalHtml'] == soal_html:
                question = q
                break
    elif lang == 'en':
        for q in quiz_data_en:
            if q['soalHtml'] == soal_html:
                question = q
                break
    
    if not question:
        return jsonify({'error': 'Question not found'}), 404
    
    # Check if answer is correct
    is_correct = question['jawaban'] == user_answer
    
    return jsonify({
        'isCorrect': is_correct,
        'penjelasan': question['penjelasan']
    })

@app.route('/api/get-flag', methods=['POST'])
def get_flag():
    from flask import request
    data = request.get_json()
    flag_counter = data.get('flagCounter', 0)
    
    # Return the flag based on counter
    if flag_counter < len(flag_data):
        return jsonify({
            'flag': flag_data[flag_counter]
        })
    else:
        return jsonify({'error': 'No more flags available'}), 404

quiz_data = [
    {
        "judul": "Contoh Email",
        "deskripsi": "Email meminta Anda untuk melakukan review pada dokumen yang tidak jelas.",
        "soalHtml": "../static/iframe-soal-id/phishing1.html",
        "jawaban": "phishing",
        "penjelasan": "Perhatikan link saat anda mengarahkan kursor diatas link dan lihat ke sebelah kiri bawah layar. Link tersebut bukan domain resmi dan meminta kredensial — ini ciri phishing."
    },
    {
        "judul": "Contoh Email",
        "deskripsi": "Email perangkat baru masuk.",
        "soalHtml": "../static/iframe-soal-id/phishing2.html",
        "jawaban": "phishing",
        "penjelasan": "Perhatikan link saat anda mengarahkan kursor diatas link dan lihat ke sebelah kiri bawah layar. \"google.real.support\" merupakan subdomain dari \"real.support\" yang bukan merupakan domain resmi Google — ini ciri phishing."
    },
    {
        "judul": "Contoh Email",
        "deskripsi": "Email mengklaim 'Seseorang mengetahui kata sandi Anda' dengan tombol 'GANTI KATA SANDI'.",
        "soalHtml": "../static/iframe-soal-id/phishing3.html",
        "jawaban": "phishing",
        "penjelasan": "Perhatikan link saat anda mengarahkan kursor diatas link dan lihat ke sebelah kiri bawah layar. Pengirim memakai alamat yang bukan domain resmi Google (contoh: no-reply@google.support.org) dan tombol mengarah ke domain asing (contoh: xyzsecurityxyz.org) namun memiliki subdomain yang menyerupai Google (contoh: myaccount.google.com-securitysettingpage.xyzsecurityxyz.org). Jangan klik tautan — ini ciri phishing."
    },
    {
        "judul": "Contoh Email",
        "deskripsi": "Email mengaku dari Dropbox dengan tombol 'LIHAT FOLDER' mungkin ini file penting?",
        "soalHtml": "../static/iframe-soal-id/phishing4.html",
        "jawaban": "phishing",
        "penjelasan": "Perhatikan link saat anda mengarahkan kursor diatas link dan lihat ke sebelah kiri bawah layar. Pengirim memakai domain yang menyerupai Dropbox (contoh: `dropbox-online.net`) tetapi bukan domain resmi `dropbox.com`. Tautan 'LIHAT FOLDER' mengarah ke domain asing (contoh: dropbox-online.net/importantfolder) yang bisa digunakan untuk mencuri kredensial atau menyebarkan malware. Jangan klik tautan; buka `dropbox.com` langsung dan periksa undangan di akun Anda — ini ciri phishing."
    },
    {
        "judul": "Contoh Email",
        "deskripsi": "Email mengklaim 'Pemberitahuan Penghentian' dari Help Desk yang mendesak pembatalan atau meminta Anda menghubungi nomor dukungan.",
        "soalHtml": "../static/iframe-soal-id/phishing5.html",
        "jawaban": "phishing",
        "penjelasan": "Pesan membuat rasa urgensi (akun akan dihentikan) dan meminta Anda menghubungi nomor atau melakukan tindakan segera, taktik umum social engineering. Alamat pengirim bisa dipalsukan (helpdesk@itss.co.id), dan nomor telepon/tautan yang diberikan dapat digunakan untuk meminta kredensial atau pembayaran. Jangan menghubungi nomor atau memberikan informasi. Verifikasi langsung ke helpdesk resmi melalui saluran yang Anda kenal (contoh: portal perusahaan atau nomor internal) — ini ciri phishing."
    },
    {
        "judul": "Contoh Pesan SMS",
        "deskripsi": "SMS mengaku dari Netflix tentang akun ditangguhkan dan menyertakan tautan pemulihan — periksa pengirim dan URL sebelum mengklik.",
        "soalHtml": "../static/iframe-soal-id/phishing6.html",
        "jawaban": "phishing",
        "penjelasan": "Pengirim menggunakan alamat/identitas yang bukan milik Netflix (contoh: netflix@mnasdfkjasdf.org) dan tautan pemulihan memakai domain yang menipu (contoh: `www.netflix.com.onlinehome.id`) yang hanya menyerupai Netflix tetapi sebenarnya berada di domain lain (onlinehome.id). Tautan seperti ini sering dipakai untuk mencuri kredensial atau memasang malware. Jangan klik tautan; buka `netflix.com` langsung atau periksa status pembayaran dari aplikasi resmi — ini ciri phishing."
    },
    {
        "judul": "Contoh Pesan SMS",
        "deskripsi": "Tiba- tiba ada yang SMS mengaku Anda pemenang undian (mis. 'Pemenang Ke-2 Shopee') dan menyertakan link pendek (bit.ly) untuk klaim hadiah. Keberuntungan?",
        "soalHtml": "../static/iframe-soal-id/phishing7.html",
        "jawaban": "phishing",
        "penjelasan": "Pesan mengklaim Anda pemenang dan memaksa tindakan cepat serta menyertakan link pendek (contoh: bit.ly/pemenangundian2) yang menyembunyikan tujuan sebenarnya. Pengirim berasal dari nomor tidak dikenal dan klaim hadiah yang tidak Anda tunggu adalah tanda umum penipuan — ini ciri phishing."
    },
    {
        "judul": "Contoh Pesan WhatsApp",
        "deskripsi": "Pesan WhatsApp berisi lampiran .apk berjudul 'Surat Undangan Pernikahan Digital'.",
        "soalHtml": "../static/iframe-soal-id/phishing8.html",
        "jawaban": "phishing",
        "penjelasan": "Berbahaya. Lampiran berformat .apk adalah paket aplikasi Android yang dapat mengandung malware. Menerima .apk lewat WhatsApp dari nomor tidak dikenal adalah tanda penipuan/malware — ini ciri phishing."
    },
    {
        "judul": "Contoh Pesan WhatsApp",
        "deskripsi": "Pesan mengaku dari instansi KEMENDIKBUD menawarkan kuota/pulsa dengan tautan domain tidak resmi.",
        "soalHtml": "../static/iframe-soal-id/phishing9.html",
        "jawaban": "phishing",
        "penjelasan": "Penipu sering memalsukan nama instansi resmi dan menggunakan domain atau tautan yang mirip (contoh: `subsidi-kuota.online` atau tautan singkat) untuk mengelabui penerima. Tanda-tanda: pengirim nomor tidak dikenal, tautan bukan domain resmi pemerintah, serta batas waktu mendesak — ini ciri phishing."
    },
    {
        "judul": "Contoh Email",
        "deskripsi": "Pemberitahuan keamanan LinkedIn tentang percobaan masuk dari perangkat baru.",
        "soalHtml": "../static/iframe-soal-id/legit1.html",
        "jawaban": "legit",
        "penjelasan": "Email ini tampak sah karena berasal dari domain resmi (`security-noreply@linkedin.com`) dan menampilkan merek/branding LinkedIn yang konsisten. Isi berisi salam personal, metadata kontekstual (tanggal, browser/perangkat), dan tautan ke Pusat Bantuan — pola yang umum pada pemberitahuan keamanan asli. Selain itu, pesan tidak meminta kredensial secara langsung atau menekan Anda untuk segera memasukkan kata sandi melalui tautan pihak ketiga."
    },
    {
        "judul": "Contoh Email",
        "deskripsi": "Newsletter Letterboxd ('Rushes') dengan header bergambar.",
        "soalHtml": "../static/iframe-soal-id/legit2.html",
        "jawaban": "legit",
        "penjelasan": "Email ini tampak sah karena menggunakan pengirim dari domain Letterboxd (`robot@letterboxd.com`) dan menampilkan branding/header yang konsisten. Tautan CTA mengarah ke `letterboxd.com` dengan parameter UTM (bukan domain asing), isi bersifat informatif (digest/summary) dan tidak meminta kredensial atau tindakan berisiko. Cara cepat memverifikasi: arahkan kursor ke tautan untuk memastikan domain adalah `letterboxd.com`, atau buka `letterboxd.com` langsung jika ragu."
    },
    {
        "judul": "Contoh Email Ad",
        "deskripsi": "Iklan bersponsor dari Android Developers yang menampilkan gambar produk dan tombol 'Learn more'.",
        "soalHtml": "../static/iframe-soal-id/legit3.html",
        "jawaban": "legit",
        "penjelasan": "Ini tampak sah sebagai iklan resmi karena menampilkan branding Android/Google yang konsisten dan tautan yang diarahkan melalui layanan iklan resmi (contoh: `googleadservices.com`) menuju halaman pengiklan. Anda juga bisa memverifikasi dengan mengunjungi situs resmi Android Developers (developer.android.com)."
    },
    {
        "judul": "Contoh Email",
        "deskripsi": "Pemberitahuan keamanan Goodreads tentang percobaan masuk ke akun Anda.",
        "soalHtml": "../static/iframe-soal-id/legit4.html",
        "jawaban": "legit",
        "penjelasan": "Email ini terlihat sah: pengirim menggunakan domain resmi (`account-update@goodreads.com`), pesan menyertakan metadata kontekstual (tanggal/waktu, perangkat, lokasi), serta tidak meminta kredensial lewat tautan pihak ketiga. Untuk memverifikasi, arahkan kursor ke tautan untuk memastikan domain adalah `goodreads.com` atau buka `goodreads.com` langsung."
    },
    {
        "judul": "Contoh Email",
        "deskripsi": "Pemberitahuan keamanan X (Twitter) tentang percobaan masuk dari perangkat baru.",
        "soalHtml": "../static/iframe-soal-id/legit5.html",
        "jawaban": "legit",
        "penjelasan": "Email ini terlihat asli karena dikirim dari domain resmi (`verify@x.com`), dan menyertakan informasi konteks (lokasi, perangkat, waktu) serta tautan tindakan resmi (mis. ubah kata sandi, tinjau aplikasi). Pesan tidak meminta kredensial lewat formulir pihak ketiga dan berisi tautan bantuan/dukungan resmi. Cara memverifikasi: arahkan kursor ke tautan untuk memastikan tujuan adalah `x.com` atau buka `x.com` langsung melalui browser."
    },
    {
        "judul": "Contoh Pesan SMS",
        "deskripsi": "SMS promosi dari myIM3 yang menawarkan fitur SATSPAM.",
        "soalHtml": "../static/iframe-soal-id/legit6.html",
        "jawaban": "legit",
        "penjelasan": "Tampak sah: pengirim menyebut 'myIM3' dan tautan menggunakan domain pendek `myim3.co` yang kemungkinan merupakan layanan resmi operator. Cara verifikasi: periksa ID pengirim/nomor apakah mirip dengan nomor layanan operator, jangan langsung memasukkan informasi lewat tautan; buka aplikasi resmi myIM3 atau kunjungi situs operator yang Anda kenal untuk mengaktifkan fitur, atau hubungi layanan pelanggan jika ragu. Hati-hati jika tautan meminta kredensial atau pembayaran di luar kanal resmi."
    },
    {
        "judul": "Contoh Pesan SMS",
        "deskripsi": "SMS dari McDonald's berisi promosi PaNas dengan tautan ke sda-ida.id.",
        "soalHtml": "../static/iframe-soal-id/legit7.html",
        "jawaban": "legit",
        "penjelasan": "Tampak sah: pesan ini berasal dari kampanye promosi resmi McDonald's Indonesia. Domain `sda-ida.id` adalah layanan URL yang berkaitan dengan Indosat Digital Analytics (iDA) dari Indosat Ooredoo. Cara verifikasi: cek apakah pengirim adalah nomor yang dikenal dari McDonald's (sering muncul sebagai 'McDonald's' di ID pengirim), periksa konsistensi branding (nama aplikasi, gaya bahasa promosi khas McD), dan pastikan tautan pendek mengarah ke domain resmi McDonald's atau aplikasi mereka. Meski legitimate, tetap berhati-hati dengan tautan pendek."
    },
    {
        "judul": "Contoh Pesan WhatsApp",
        "deskripsi": "Pesan WhatsApp dari akun terverifikasi dengan tanda centang hijau, menawarkan promosi belanja.",
        "soalHtml": "../static/iframe-soal-id/legit8.html",
        "jawaban": "legit",
        "penjelasan": "Tampak sah: pesan ini berasal dari akun WhatsApp Business resmi yang terverifikasi (ditandai dengan centang hijau ✓ di samping nama pengirim). Tanda verifikasi hijau adalah fitur resmi WhatsApp yang hanya diberikan kepada akun bisnis yang telah diverifikasi identitasnya oleh WhatsApp. Pesan berisi promosi belanja dengan personalisasi nama penerima, gaya bahasa marketing yang konsisten dengan brand Cara verifikasi: pastikan ada centang hijau verifikasi di nama pengirim, periksa apakah nama akun cocok dengan brand resmi, cek riwayat chat sebelumnya dengan nomor yang sama, dan jika ada tautan, pastikan mengarah ke domain resmi perusahaan. Meski legitimate, tetap berhati-hati — jangan langsung klik tautan tanpa memverifikasi tujuan URL."
    },
    {
        "judul": "Contoh Pesan WhatsApp",
        "deskripsi": "Pesan WhatsApp dari akun terverifikasi dengan tanda centang hijau, menawarkan promosi berlangganan.",
        "soalHtml": "../static/iframe-soal-id/legit9.html",
        "jawaban": "legit",
        "penjelasan": "Tampak sah: pesan ini berasal dari akun WhatsApp Business resmi yang terverifikasi (ditandai dengan centang hijau ✓ di samping nama pengirim 'Gojek Indonesia'). Tanda verifikasi hijau adalah fitur resmi WhatsApp yang hanya diberikan kepada akun bisnis yang telah diverifikasi identitasnya oleh WhatsApp. Pesan berisi promosi re-subscription Gojek PLUS dengan personalisasi nama penerima ('John Doe, gak usah gengsi...😉'), menyebutkan benefit spesifik layanan (diskon GoFood, GoRide, GoCar, GoMart s.d. 10rb/8rb), dan menggunakan gaya bahasa marketing informal yang konsisten dengan brand Gojek. Cara verifikasi: pastikan ada centang hijau verifikasi di nama pengirim, periksa apakah nama akun cocok dengan brand resmi ('Gojek Indonesia'), cek riwayat chat sebelumnya dengan nomor yang sama untuk melihat pesan-pesan sebelumnya dari Gojek, dan jika ada tautan, verifikasi mengarah ke domain resmi atau dalam aplikasi. Meski legitimate, tetap berhati-hati."
    }
]

quiz_data_en = [
    {
        "judul": "Email Example",
        "deskripsi": "Email asking you to review an unclear document.",
        "soalHtml": "../static/iframe-soal-en/phishing1.html",
        "jawaban": "phishing",
        "penjelasan": "Notice the link when you hover your cursor over it and look at the bottom left of the screen. The link is not an official domain and requests credentials — this is a phishing characteristic."
    },
    {
        "judul": "Email Example",
        "deskripsi": "Email about new device login.",
        "soalHtml": "../static/iframe-soal-en/phishing2.html",
        "jawaban": "phishing",
        "penjelasan": "Notice the link when you hover your cursor over it and look at the bottom left of the screen. \"google.real.support\" is a subdomain of \"real.support\" which is not an official Google domain — this is a phishing characteristic."
    },
    {
        "judul": "Email Example",
        "deskripsi": "Email claiming 'Someone knows your password' with a 'CHANGE PASSWORD' button.",
        "soalHtml": "../static/iframe-soal-en/phishing3.html",
        "jawaban": "phishing",
        "penjelasan": "Notice the link when you hover your cursor over it and look at the bottom left of the screen. The sender uses an address that is not an official Google domain (example: no-reply@google.support.org) and the button points to a foreign domain (example: xyzsecurityxyz.org) but has a subdomain resembling Google (example: myaccount.google.com-securitysettingpage.xyzsecurityxyz.org). Don't click the link — this is a phishing characteristic."
    },
    {
        "judul": "Email Example",
        "deskripsi": "Email claiming to be from Dropbox with a 'VIEW FOLDER' button - could this be an important file?",
        "soalHtml": "../static/iframe-soal-en/phishing4.html",
        "jawaban": "phishing",
        "penjelasan": "Notice the link when you hover your cursor over it and look at the bottom left of the screen. The sender uses a domain resembling Dropbox (example: `dropbox-online.net`) but not the official `dropbox.com` domain. The 'VIEW FOLDER' link points to a foreign domain (example: dropbox-online.net/importantfolder) that could be used to steal credentials or spread malware. Don't click the link; go directly to `dropbox.com` and check invitations in your account — this is a phishing characteristic."
    },
    {
        "judul": "Email Example",
        "deskripsi": "Email claiming 'Suspension Notice' from Help Desk urging cancellation or asking you to contact support number.",
        "soalHtml": "../static/iframe-soal-en/phishing5.html",
        "jawaban": "phishing",
        "penjelasan": "The message creates urgency (account will be suspended) and asks you to call a number or take immediate action, a common social engineering tactic. The sender's address can be forged (helpdesk@itss.co.id), and the phone number/link provided can be used to request credentials or payment. Don't call the number or provide information. Verify directly with the official helpdesk through channels you know (example: company portal or internal number) — this is a phishing characteristic."
    },
    {
        "judul": "SMS Example",
        "deskripsi": "SMS claiming to be from Netflix about suspended account with recovery link — check sender and URL before clicking.",
        "soalHtml": "../static/iframe-soal-en/phishing6.html",
        "jawaban": "phishing",
        "penjelasan": "The sender uses an address/identity not belonging to Netflix (example: netflix@mnasdfkjasdf.org) and the recovery link uses a deceptive domain (example: `www.netflix.com.onlinehome.id`) that only resembles Netflix but is actually on another domain (onlinehome.id). Links like this are often used to steal credentials or install malware. Don't click the link; go directly to `netflix.com` or check payment status from the official app — this is a phishing characteristic."
    },
    {
        "judul": "SMS Example",
        "deskripsi": "Suddenly receiving SMS claiming you won a lottery (e.g., 'Shopee Winner #2') with a short link (bit.ly) to claim prize. Lucky day?",
        "soalHtml": "../static/iframe-soal-en/phishing7.html",
        "jawaban": "phishing",
        "penjelasan": "The message claims you're a winner and forces quick action while including a short link (example: bit.ly/pemenangundian2) that hides the real destination. The sender is from an unknown number and unexpected prize claims are common signs of fraud — this is a phishing characteristic."
    },
    {
        "judul": "WhatsApp Example",
        "deskripsi": "WhatsApp message containing .apk attachment titled 'Digital Wedding Invitation'.",
        "soalHtml": "../static/iframe-soal-en/phishing8.html",
        "jawaban": "phishing",
        "penjelasan": "Dangerous. Attachments in .apk format are Android application packages that can contain malware. Receiving .apk via WhatsApp from unknown numbers is a sign of fraud/malware — this is a phishing characteristic."
    },
    {
        "judul": "WhatsApp Example",
        "deskripsi": "Message claiming to be from KEMENDIKBUD institution offering data/credit quota with unofficial domain link.",
        "soalHtml": "../static/iframe-soal-en/phishing9.html",
        "jawaban": "phishing",
        "penjelasan": "Scammers often impersonate official institutions and use similar domains or links (example: `subsidi-kuota.online` or short links) to deceive recipients. Signs: sender from unknown number, link is not official government domain, and urgent deadline — this is a phishing characteristic."
    },
    {
        "judul": "Email Example",
        "deskripsi": "LinkedIn security notification about login attempt from new device.",
        "soalHtml": "../static/iframe-soal-en/legit1.html",
        "jawaban": "legit",
        "penjelasan": "This email appears legitimate because it comes from an official domain (`security-noreply@linkedin.com`) and displays consistent LinkedIn branding. The content includes a personal greeting, contextual metadata (date, browser/device), and links to Help Center — patterns common in genuine security notifications. Additionally, the message does not directly request credentials or pressure you to immediately enter a password through a third-party link."
    },
    {
        "judul": "Email Example",
        "deskripsi": "Letterboxd newsletter ('Rushes') with illustrated header.",
        "soalHtml": "../static/iframe-soal-en/legit2.html",
        "jawaban": "legit",
        "penjelasan": "This email appears legitimate because it uses a sender from the Letterboxd domain (`robot@letterboxd.com`) and displays consistent branding/header. CTA links point to `letterboxd.com` with UTM parameters (not foreign domains), the content is informative (digest/summary) and does not request credentials or risky actions. Quick verification: hover cursor over links to ensure the domain is `letterboxd.com`, or go directly to `letterboxd.com` if in doubt."
    },
    {
        "judul": "Email Ad Example",
        "deskripsi": "Sponsored ad from Android Developers showing product image and 'Learn more' button.",
        "soalHtml": "../static/iframe-soal-en/legit3.html",
        "jawaban": "legit",
        "penjelasan": "This appears legitimate as an official ad because it displays consistent Android/Google branding and links directed through official ad services (example: `googleadservices.com`) to the advertiser's page. You can also verify by visiting the official Android Developers site (developer.android.com)."
    },
    {
        "judul": "Email Example",
        "deskripsi": "Goodreads security notification about login attempt to your account.",
        "soalHtml": "../static/iframe-soal-en/legit4.html",
        "jawaban": "legit",
        "penjelasan": "This email appears legitimate: the sender uses an official domain (`account-update@goodreads.com`), the message includes contextual metadata (date/time, device, location), and does not request credentials through third-party links. To verify, hover cursor over links to ensure the domain is `goodreads.com` or go directly to `goodreads.com`."
    },
    {
        "judul": "Email Example",
        "deskripsi": "X (Twitter) security notification about login attempt from new device.",
        "soalHtml": "../static/iframe-soal-en/legit5.html",
        "jawaban": "legit",
        "penjelasan": "This email appears genuine because it's sent from an official domain (`verify@x.com`), and includes contextual information (location, device, time) as well as official action links (e.g., change password, review apps). The message does not request credentials through third-party forms and contains official help/support links. Verification method: hover cursor over links to ensure destination is `x.com` or go directly to `x.com` via browser."
    },
    {
        "judul": "SMS Example",
        "deskripsi": "Promotional SMS from myIM3 offering SATSPAM feature.",
        "soalHtml": "../static/iframe-soal-en/legit6.html",
        "jawaban": "legit",
        "penjelasan": "Appears legitimate: sender mentions 'myIM3' and link uses short domain `myim3.co` which is likely an official operator service. Verification method: check sender ID/number if it matches operator service numbers, don't immediately enter information through links; open official myIM3 app or visit the operator site you know to activate features, or contact customer service if in doubt. Be careful if link requests credentials or payment outside official channels."
    },
    {
        "judul": "SMS Example",
        "deskripsi": "SMS from McDonald's containing PaNas promotion with link to sda-ida.id.",
        "soalHtml": "../static/iframe-soal-en/legit7.html",
        "jawaban": "legit",
        "penjelasan": "Appears legitimate: this message comes from an official McDonald's Indonesia promotional campaign. The domain `sda-ida.id` is a URL service related to Indosat Digital Analytics (iDA) from Indosat Ooredoo. Verification method: check if sender is a known McDonald's number (often appears as 'McDonald's' in sender ID), verify branding consistency (app name, typical McD promotional language style), and ensure short link points to official McDonald's domain or their app. Even though legitimate, remain cautious with short links."
    },
    {
        "judul": "WhatsApp Example",
        "deskripsi": "WhatsApp message from verified account with green checkmark, offering shopping promotion.",
        "soalHtml": "../static/iframe-soal-en/legit8.html",
        "jawaban": "legit",
        "penjelasan": "Appears legitimate: this message comes from an official verified WhatsApp Business account (marked with green checkmark ✓ next to sender name). The green verification badge is an official WhatsApp feature only given to business accounts whose identity has been verified by WhatsApp. The message contains shopping promotion with recipient name personalization, marketing language style consistent with the brand. Verification method: ensure there's a green verification checkmark on sender name, check if account name matches official brand, review previous chat history with the same number, and if there are links, ensure they point to the company's official domain. Even though legitimate, remain cautious — don't immediately click links without verifying URL destination."
    },
    {
        "judul": "WhatsApp Example",
        "deskripsi": "WhatsApp message from verified account with green checkmark, offering subscription promotion.",
        "soalHtml": "../static/iframe-soal-en/legit9.html",
        "jawaban": "legit",
        "penjelasan": "Appears legitimate: this message comes from an official verified WhatsApp Business account (marked with green checkmark ✓ next to sender name 'Gojek Indonesia'). The green verification badge is an official WhatsApp feature only given to business accounts whose identity has been verified by WhatsApp. The message contains Gojek PLUS re-subscription promotion with recipient name personalization ('John Doe, gak usah gengsi...😉'), mentions specific service benefits (GoFood, GoRide, GoCar, GoMart discounts up to 10k/8k), and uses informal marketing language style consistent with Gojek brand. Verification method: ensure there's a green verification checkmark on sender name, check if account name matches official brand ('Gojek Indonesia'), review previous chat history with the same number to see previous Gojek messages, and if there are links, verify they point to official domain or in-app. Even though legitimate, remain cautious."
    }
]

flag_data = [
    '4OENjTeS1C',
    'Dh3mJX8r4T',
    'jjI2a1Iqdf',
    'wQJSYi0WoK',
    'JKsn22reZh',
    'CBomPh3lYA',
    'r37Ly2dNKY',
    'X8MvFX4pxD',
    'lRMxffSDvR',
    'YElHNicvoh',
    'Jlrdp8QGLF'
]

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
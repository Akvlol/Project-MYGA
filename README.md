# MYGA - Make Youtube Great Again

Tạo 1 playlist local.

---

## I. Vấn đề của youtube tao thấy chướng mắt:

* Video được gắn mác **"Dành cho trẻ em, Youtube Kids"** sẽ không thể add vào playlist.
* Các bài nhạc chứa nội dung bạo lực, tự hại sẽ bắt phải confirm mỗi lần mở mới cho nghe (aka không tự phát dù đã bật autoplay).
* Người dùng khó biết video nào đã bị xoá, bị gỡ khỏi playlist, khiến cho việc tìm video thay thế rất khó khăn và phiền phức.
* Khi nhấn 2 lần nút trên tai nghe, thay vì nhảy sang video khác trong playlist, lại nhảy ra video khác trong phần suggestion - ngoài playlist.
* Tính năng shuffle của youtube playlist **KHÔNG DẢM BẢO** bạn sẽ nghe được tất cả bài trong playlist một cách auto.

> **Note:** Tao dùng youtube (không premium) qua Brave browser cả trên Laptop (CachyOS KDE) và cả điện thoại (Android 13), nên các vấn đề tao gặp có thể sẽ khác với các bạn.

---

## II. Project này đã làm được gì?

### 1. Lưu playlist local dạng JSON

* CURD các thứ, có thể edit thủ công trong file `playlist.json`.

=> Khi video youtube bị xoá, ta vẫn biết title của video.

### 2. Điều khiển browser, chạy bài hát bằng link

* Next
* Previous
* Pause
* Play thủ công.
* Jump to nhảy đến bài tự chọn.
* Shuffle đảm bảo có thể phát mọi bài hát từ đầu tới cuối.

=> Phát được video "dành cho trẻ em".

=> Bypass confirmation của video bạo lực / tự hại bằng cách gọi thẳng link phát của video.

---

## III. Các vấn đề / hạn chế ở hiện tại - sẽ phát triển thêm nếu thích:

* UXUI grub còn lỏ.
* Vài tính năng như `jump_to` không thể back về nếu thay đổi quyết định giữa chừng.
* Chưa giải quyết vấn đề về nút trên tai nghe.
* **Chỉ mới test trên CachyOS KDE Linux**, chưa test trên bất kỳ hđh nào khác.
* Dự kiến sẽ tìm cách để nó chạy được trên điện thoại.

---

## IV. Cách chạy hệ thống và các thứ kèm theo:

Hệ thống chỉ mới có thể chạy trên **Linux**.

Chỉ mới test trên **CachyOS KDE**.

### Để có thể chạy được ngay:

#### 1. Brave browser

Cài Brave browser, hoặc chỉnh hằng `BROWSER` trong `browser_manager.py`.

#### 2. `kdotool` / `xdotool` — Optional

Cài `kdotool` nếu dùng KDE Wayland gì đó.

Nếu dùng X11 thì cài `xdotool` và thay chữ `kdotool` trong `browser_manager.py` thành `xdotool`.

=> Cái này chủ yếu là phục vụ chức năng tự động minimize browser window khi bắt đầu play.

#### 3. Chạy chương trình

Chạy `main.py` bằng lệnh python trong môi trường **`.venv`**, vì tao đã làm thế.

```bash
source .venv/bin/activate
python main.py
```

---

## Project Status

Hiện tại project vẫn đang trong quá trình phát triển.

Những thứ dự kiến sẽ làm nếu thích:

* UXUI đỡ grub hơn.
* Fix `jump_to`.
* Xử lý nút trên tai nghe.
* Detect video end để tự động next.
* Tìm cách chạy được trên điện thoại.
* Test thêm trên các hđh khác.

---

## Tech Stack

* Python
* JSON
* Brave Browser
* Chrome DevTools Protocol (CDP)
* Linux
* CachyOS KDE

```
- Formatted README.md by ChatGPT, because tao format xấu như chó
- Code phần lớn bởi tao
- Có vibe JS và một số chức năng khác cùng ChatGPT, Claude vì tao đéo biết code JS
- Fix bug bằng Claude
```

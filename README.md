# 个人主页

基于 [al-folio](https://github.com/alshedivat/al-folio)（MIT）的中英双语个人主页，托管在 GitHub Pages。

## 双语结构

英文版在 `/`，中文版在 `/zh/`，导航栏右侧的「中文 / EN」按钮互相跳转。

| 内容 | 英文 | 中文 |
| --- | --- | --- |
| 首页 | `_pages/about.md` | `_pages/zh/about.md` |
| 简历页 | `_pages/cv.md` | `_pages/zh/cv.md` |
| 简历数据 | `_data/cv.yml` | `_data/cv_zh.yml` |
| 博客 | `_pages/blog.md`（两种语言共用） | 同左 |

每个页面靠 front matter 里的三个字段参与双语逻辑：

- `lang`：`en` / `zh` / `all`，决定它出现在哪个语言的导航栏（`all` 表示两边都出现）
- `lang_alt`：对应语言版本的 URL，语言切换按钮据此生成；不写就不显示按钮
- `title_zh`：仅 `lang: all` 的页面需要，让中文导航栏不至于混英文标签

中文简历 `_data/cv_zh.yml` 里的小节 key 仍用英文（`Education`、`Skills` 等），
渲染时会自动转换成中文标题，这样中英文两份数据共用同一套渲染模板。
`end_date` 写 `至今` 会原样显示，写 `present` 则显示 `PRESENT`。

### 覆盖了哪些主题文件

al-folio v1.x 的模板打包在 gem 里，本地同名文件会覆盖它。为实现双语，仓库内覆盖了 4 个：

| 文件 | 改动 |
| --- | --- |
| `_includes/header.liquid` | 按语言过滤导航项、语言切换按钮、中文页用 `name_zh` 作品牌名 |
| `_layouts/about.liquid` | 中文页标题用 `name_zh`，「最新文章」等栏目名本地化 |
| `_includes/footer.liquid` | 中文页版权署名用 `name_zh` |
| `_includes/cv/render.liquid` | 支持 `cv_data` 指定数据源、小节标题中文化（并移除了用不到的 JSONResume 分支） |

**升级 al-folio 时要留意这 4 个文件**，上游若改了它们，需要手工合并。删掉本地文件即可回退到主题默认行为。

已知取舍：浏览器标签页标题（`<title>`）在中文页仍显示 `Ziyang Chen`，
因为它由 gem 内 247 行的 `metadata.liquid` 生成，为一行署名覆盖整个文件不划算。

## 常改的地方

| 位置 | 改什么 |
| --- | --- |
| `_config.yml` | `first_name` / `last_name` / `name_zh`、`url`、`description` |
| `_pages/about.md`、`_pages/zh/about.md` | `subtitle`、头像旁的 `profile.more_info`、正文自我介绍 |
| `_data/socials.yml` | `email`、`github_username`；**不用的项必须整行注释，留空值会导致构建失败** |
| `_data/cv.yml`、`_data/cv_zh.yml` | 教育、实习、项目、奖项、技能 |
| `assets/img/prof_pic.jpg` | 换成本人照片（正方形，800×800 以内即可） |

`baseurl` 必须留空，仓库名为 `用户名.github.io` 的用户站点不需要子路径。

## 隐私约定

- 手机号一律不出现在本仓库任何文件里。
- `CV/` 目录已在 `.gitignore` 中，用于存放**未脱敏**的简历原件，不会被提交。
  要对外提供 PDF 版简历，请先删掉手机号等私密信息，再放到 `assets/pdf/`，
  并在 `_data/socials.yml` 的 `cv_pdf` 与 `_pages/cv.md` 里填路径。
- `Figure/` 同样已忽略，放原图。上站的图片请压缩后放 `assets/img/`：

  ```bash
  magick Figure/原图.jpg -resize 1000x -strip -quality 86 assets/img/名字.jpg
  ```

  CV 里的配图直接写在 `highlights` 条目内（该字段会走 markdownify，可混用 Markdown
  链接和 `<img>`），因此不必改模板。用 `style="max-width:min(100%,300px)"` 之类限制宽度。

  kramdown 的规矩要留意：块级标签（`<div>`、`<details>`）**必须独占一个 highlight
  条目、出现在开头**，才会被当成 HTML；一旦跟在文字后面，就会被转义成字面文本显示出来。
  照片因此都包在自己的条目里，用 `<details><summary>` 做成点击展开，多张图靠
  `display:inline-block` 并排（同一条目内的 `<img>` 是内联元素，可以紧跟文字）。

  时间轴左侧那列只有约 104px 宽，`location` 太长会溢出。该字段原样输出不转义，
  可以直接用 `<br>` 手动折行（见高中条目）。
- 实习内容按方向描述，不写内部模型名、性能对比数字和同事姓名。

## 本地预览

需要 Docker，不用装 Ruby。容器内 Jekyll 固定监听 8080，把它映射到宿主机一个空闲端口即可
（这台开发机的 8080 长期被别的服务占用，所以用 4001）：

```bash
docker run --rm --name alfolio -p 4001:8080 -v "$PWD":/srv/jekyll \
  -e JEKYLL_ENV=development amirpourmand/al-folio:latest \
  /srv/jekyll/bin/entry_point.sh
```

改动会自动重建，刷新浏览器即可看到。结束用 `Ctrl-C`，或另开终端 `docker rm -f alfolio`。

装了 compose 插件的话，`docker compose up` 也可以，但它按 `docker-compose.yml` 走 8080:8080。

### 在远程开发机上预览

服务器上的 `localhost:4001` 不等于你本机的 `localhost:4001`，需要先打通网络，任选一种：

- Cursor / VS Code 底部 **PORTS** 面板手动 Forward 端口 `4001`
- 直接访问服务器内网地址 `http://<服务器IP>:4001`
- 本机开隧道：`ssh -N -L 4001:localhost:4001 <user>@<服务器IP>`

验证服务本身是否正常，在服务器上跑 `curl -I http://localhost:4001`，返回 200 就说明站点没问题，打不开纯属转发没通。

## 部署

推到 `main` 分支后，`.github/workflows/deploy.yml` 会自动构建并把产物推到 `gh-pages` 分支。首次推送后需要去仓库 **Settings → Pages**，把 Source 设为 **Deploy from a branch**，分支选 **`gh-pages`**、目录选 `/ (root)`。

## 日常维护

- 博客：在 `_posts/` 下新建 `YYYY-MM-DD-slug.md`
- 论文：在 `_bibliography/papers.bib` 加 BibTeX 条目，并把 `_pages/publications.md` 的 `nav` 改成 `true`
- 动态：在 `_news/` 下新建 `.md`，并把两个 `about.md` 里的 `announcements.enabled` 改成 `true`
- 项目 / 教学 / 书架：分别对应 `_projects/`、`_teachings/`、`_books/`，同样是加文件后打开对应页面的 `nav`

这些页面的文件都已保留，默认只是从导航栏里隐藏了。论文页在投稿双盲期间保持关闭。

`_bibliography/papers.bib` 里**不要留被注释掉的 BibTeX 条目**：解析器看到 `@` 就会开始解析，
即使前面有 `%` 也一样，会直接导致构建失败。

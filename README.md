# 个人主页

基于 [al-folio](https://github.com/alshedivat/al-folio)（MIT）的个人主页，托管在 GitHub Pages。

## 首次上线前需要改的地方

按顺序改完这几处就能上线，其余保持默认即可：

| 位置 | 改什么 |
| --- | --- |
| `_config.yml` | `first_name` / `last_name`、`url`（把 `YOUR-GITHUB-USERNAME` 换成自己的 GitHub 用户名）、`description` |
| `_pages/about.md` | `subtitle`、`profile.more_info` 里的单位地址，以及正文自我介绍 |
| `_data/socials.yml` | `email`、`github_username`，其余想显示的图标取消注释 |
| `_data/cv.yml` | 教育经历、工作经历、技能 |
| `assets/img/prof_pic.jpg` | 换成自己的照片（正方形，建议 800×800 以内） |

`baseurl` 必须留空，仓库名为 `用户名.github.io` 的用户站点不需要子路径。

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
- 动态：在 `_news/` 下新建 `.md`，并把 `_pages/about.md` 里 `announcements.enabled` 改成 `true`
- 项目 / 教学 / 书架：分别对应 `_projects/`、`_teachings/`、`_books/`，同样是加文件后打开对应页面的 `nav`

这些页面的文件都已保留，默认只是从导航栏里隐藏了。

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

需要 Docker，不用装 Ruby：

```bash
docker compose up
```

然后打开 <http://localhost:8080>。改动会自动重建，刷新即可看到。结束后 `Ctrl-C`，或者 `docker compose down`。

如果环境里没有 compose 插件，等价的原始命令是：

```bash
docker run --rm --name alfolio -p 8080:8080 -v "$PWD":/srv/jekyll \
  -e JEKYLL_ENV=development amirpourmand/al-folio:latest \
  /srv/jekyll/bin/entry_point.sh
```

## 部署

推到 `main` 分支后，`.github/workflows/deploy.yml` 会自动构建并把产物推到 `gh-pages` 分支。首次推送后需要去仓库 **Settings → Pages**，把 Source 设为 **Deploy from a branch**，分支选 **`gh-pages`**、目录选 `/ (root)`。

## 日常维护

- 博客：在 `_posts/` 下新建 `YYYY-MM-DD-slug.md`
- 论文：在 `_bibliography/papers.bib` 加 BibTeX 条目，并把 `_pages/publications.md` 的 `nav` 改成 `true`
- 动态：在 `_news/` 下新建 `.md`，并把 `_pages/about.md` 里 `announcements.enabled` 改成 `true`
- 项目 / 教学 / 书架：分别对应 `_projects/`、`_teachings/`、`_books/`，同样是加文件后打开对应页面的 `nav`

这些页面的文件都已保留，默认只是从导航栏里隐藏了。

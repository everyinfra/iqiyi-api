# iQIYI API（爱奇艺 API）

[English](#english) · [中文](#中文)

## English

This repo reads public iQIYI data with Python or curl. You can search videos by keyword, read the details of one video, and look up a series on the international site with its episodes and cast. You need one EveryInfra API key. You do not need an iQIYI account or cookie. The same API also works as an MCP tool in Claude and Cursor. Billing is per call: these 3 capabilities cost $1.39 per 1,000 calls (about $0.0014 per call). Failed calls and empty results are not charged. The EveryInfra iQIYI API has 3 capabilities, all listed on the platform page: <https://everyinfra.com/en/iqiyi-api?utm_source=github&utm_medium=example_repo&utm_campaign=iqiyi-api>

### Quick start

```bash
git clone https://github.com/everyinfra/iqiyi-api.git
cd iqiyi-api
pip install -r requirements.txt
export EVERYINFRA_API_KEY=<your API key>
python main.py search 纪录片 --out videos.csv
python main.py video "<video url>" --out video.json
python main.py album 苍兰诀 --out album.json
```

- `video` takes only play page links that start with v_ (for example https://www.iqiyi.com/v_<id>.html). Use the `url` from a `search` result. Album pages that start with a_ do not work.
- `album` looks up a series on the iQIYI international site by title. Pass the title, not a link.
- Without `--out`, the command prints the first 3 rows as JSON. With `--out`, it saves a .csv or .json file. The CSV has a BOM, so Excel opens it without garbled text.
- Register at everyinfra.com, then create the API key in the console. Steps: <https://everyinfra.com/en/docs?utm_source=github&utm_medium=example_repo&utm_campaign=iqiyi-api#quickstart>

### curl

```bash
curl -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"platform":"iqiyi","action":"search","params":{"keyword":"纪录片"}}'
```

All capabilities use the same URL. Change `action` and `params` to call another one. Examples for `video` and `album` are in [examples/curl.sh](examples/curl.sh).

### Claude and Cursor (MCP)

The remote MCP URL is <https://api.everyinfra.com/mcp>. Add the `Authorization: Bearer` header with your API key. EveryInfra runs the server, so you install no local program.

Claude Code:

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp --header "Authorization: Bearer <API Key>"
```

Cursor and other clients that read `mcp.json` ([examples/mcp.json](examples/mcp.json)):

```json
{
  "mcpServers": {
    "everyinfra": {
      "url": "https://api.everyinfra.com/mcp",
      "headers": {
        "Authorization": "Bearer <API Key>"
      }
    }
  }
}
```

Custom connectors in Claude on the web and desktop, and ChatGPT, accept only a URL. Enter <https://api.everyinfra.com/mcp/all>, sign in to EveryInfra when asked, and allow access. You do not need to enter a key. Full steps: <https://everyinfra.com/en/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=iqiyi-api>

### Price

| `action` | Per 1,000 calls |
|---|---|
| `search` | $1.39 |
| `video` | $1.39 |
| `album` | $1.39 |

- Billing is per call, about $0.0014 each. Failed calls, empty results, parameter errors, and authentication failures are not charged.
- A new account gets a $1 trial allowance, valid for 24 hours. No credit card is needed. How to claim it: <https://everyinfra.com/en/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=iqiyi-api>

### Fields

These are the fields that the 3 capabilities returned in our test. Each meaning is the first sentence of the field's entry in the API documentation. The link under each table has the full text.

#### `search` (keyword search)

| Field | Meaning |
|---|---|
| `id` | The record's unique ID on the platform. |
| `url` | Link to the record on the platform. |
| `title` | Title. null when the platform has no titles (for example text-only posts). |
| `category` | Category name in the platform's own taxonomy, not normalized across platforms. |
| `category_id` | Category ID. |
| `duration_seconds` | Duration in seconds. null for content that is not video or audio. |
| `heat_count` | iQIYI heat value. **It is a platform-specific metric, not a play count**, and cannot be compared across platforms. |
| `like_count` | Likes. null means the platform or this capability does not disclose it; it is not 0. |
| `comment_count` | Comments. null means not disclosed, not 0. |
| `collect_count` | Saves or favorites. null means not disclosed, not 0. |
| `image_url` | Image link. |
| `wide_image_url` | Landscape poster. |
| `author_name` | Author's display name. |
| `author_id` | Author's unique ID on the platform. |
| `author_avatar_url` | Uploader avatar (search / video). |
| `author_follower_count` | Author's follower count. null means not disclosed. |
| `author_video_count` | Number of videos the author has published. |
| `duration_sec` | Duration in seconds, the same value as duration_seconds (both names are returned). |
| `posted_at` | Publish time in ISO 8601, UTC (for example 2026-08-07T12:34:56+00:00). |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `author_location` | Uploader location, as written on the page (search / video). |
| `author_org` | Verified organization name (for organization accounts). |

All parameters and fields: <https://everyinfra.com/en/iqiyi-api/search?utm_source=github&utm_medium=example_repo&utm_campaign=iqiyi-api>

#### `video` (video details)

| Field | Meaning |
|---|---|
| `id` | The record's unique ID on the platform. |
| `url` | Link to the record on the platform. |
| `title` | Title. null when the platform has no titles (for example text-only posts). |
| `category` | Category name in the platform's own taxonomy, not normalized across platforms. |
| `category_id` | Category ID. |
| `heat_count` | iQIYI heat value. **It is a platform-specific metric, not a play count**, and cannot be compared across platforms. |
| `like_count` | Likes. null means the platform or this capability does not disclose it; it is not 0. |
| `comment_count` | Comments. null means not disclosed, not 0. |
| `collect_count` | Saves or favorites. null means not disclosed, not 0. |
| `image_url` | Image link. |
| `wide_image_url` | Landscape poster. |
| `author_name` | Author's display name. |
| `author_id` | Author's unique ID on the platform. |
| `author_avatar_url` | Uploader avatar (search / video). |
| `author_follower_count` | Author's follower count. null means not disclosed. |
| `author_video_count` | Number of videos the author has published. |
| `author_location` | Uploader location, as written on the page (search / video). |
| `author_org` | Verified organization name (for organization accounts). |
| `posted_at` | Publish time in ISO 8601, UTC (for example 2026-08-07T12:34:56+00:00). |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |

All parameters and fields: <https://everyinfra.com/en/iqiyi-api/video?utm_source=github&utm_medium=example_repo&utm_campaign=iqiyi-api>

#### `album` (album)

| Field | Meaning |
|---|---|
| `id` | The record's unique ID on the platform. |
| `url` | Link to the record on the platform. |
| `play_url` | Playback page link. |
| `title` | Title. null when the platform has no titles (for example text-only posts). |
| `type` | Record type; values depend on the capability (for example video / image / text). |
| `is_series` | Whether it is a series (as opposed to a single film). |
| `year` | Year. |
| `release_date` | Release date. |
| `episode_count` | Number of episodes. |
| `episode_available_count` | Number of episodes currently available to watch. |
| `image_url` | Image link. |
| `episodes` | List of episodes. |
| `cast` | Cast list. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `subtitle` | Subtitle. |
| `duration_seconds` | Duration in seconds. null for content that is not video or audio. |
| `rating` | Rating. **The scale varies by platform**: rating_scale on the same row gives the maximum (usually 5; Booking, Douban, iQIYI and NAVER use 10). |
| `content_rating` | Content rating. |
| `duration_sec` | Duration in seconds, the same value as duration_seconds (both names are returned). |
| `rating_scale` | Maximum of rating in the same row: 5 for five-star scales, 10 for ten-point scales. |

All parameters and fields: <https://everyinfra.com/en/iqiyi-api/album?utm_source=github&utm_medium=example_repo&utm_campaign=iqiyi-api>

### FAQ

**Do I need an iQIYI account or cookie to call the API?**

No. Send the `Authorization: Bearer` header with your API key. The request body holds `platform`, `action`, and the capability parameters. You do not scan a QR code, keep a login session, or open a browser.

**How much does it cost? Are failed calls charged? Is there a free allowance?**

Billing is per call, from $1.39 per 1,000 calls. Failed calls, empty results, parameter errors, and authentication failures are not charged. A new account gets a $1 trial allowance, valid for 24 hours. No credit card is needed. How to claim it: <https://everyinfra.com/en/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=iqiyi-api>

**Can I connect the iQIYI API to Claude or Cursor?**

Yes. The remote MCP URL is <https://api.everyinfra.com/mcp>. Add the `Authorization: Bearer` header with your API key. You install no local program. Setup for Claude, Cursor, ChatGPT, and Claude Code: <https://everyinfra.com/en/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=iqiyi-api>.

**What legal points apply when I use iQIYI data?**

The EveryInfra Terms of Service require you to make sure your use of the data follows applicable law and the terms of the relevant platform. Do not use the data for anything illegal or anything that violates privacy or intellectual property rights. Do not use bulk scraping for harassment, fraud, or other abuse. When you use personal information such as nicknames and avatars, keep only the fields your business needs.

**Which iQIYI data can I get?**

The EveryInfra iQIYI API has 3 capabilities:

- keyword search
- video details
- album

Parameters and return fields for each capability are on the platform page: <https://everyinfra.com/en/iqiyi-api?utm_source=github&utm_medium=example_repo&utm_campaign=iqiyi-api>

### Tested

Before release, we ran the 3 commands in Quick start against the live API with this repo's code.

| Command | Time (Singapore, UTC+8) | Rows | Charged |
|---|---|---|---|
| `python main.py search 纪录片 --out videos.csv` | 2026-11-21 09:37 | 20 | $0.001389 |
| `python main.py video "<video url>" --out video.json` | 2026-11-21 09:38 | 1 | $0.001389 |
| `python main.py album 苍兰诀 --out album.json` | 2026-11-21 09:43 | 10 | $0.001389 |

## 中文

本仓库用 Python 或 curl 读爱奇艺公开数据：按关键词搜视频，读单条视频详情，按剧名查国际站专辑的分集和演员。只需一把 EveryInfra API Key，不用爱奇艺账号和 Cookie，也能作为 MCP 工具接进 Claude、Cursor。按调用次数计费，这 3 个能力每千次 $1.39（每次约 $0.0014），失败和空结果不收费。爱奇艺共 3 个能力：<https://everyinfra.com/iqiyi-api?utm_source=github&utm_medium=example_repo&utm_campaign=iqiyi-api>

### 快速开始

```bash
git clone https://github.com/everyinfra/iqiyi-api.git
cd iqiyi-api
pip install -r requirements.txt
export EVERYINFRA_API_KEY=<你的 API Key>
python main.py search 纪录片 --out videos.csv
python main.py video "<视频链接>" --out video.json
python main.py album 苍兰诀 --out album.json
```

- `video` 只收 v_ 开头的播放页链接（形如 https://www.iqiyi.com/v_<ID>.html），用 `search` 结果里的 `url`；专辑页 a_ 开头的链接不能用。
- `album` 按剧名查爱奇艺国际站的专辑，传剧名，不传链接。
- 不加 `--out` 时打印前 3 条 JSON；加 `--out` 存成 .csv 或 .json。CSV 带 BOM，Excel 直接打开不乱码。
- API Key 在 everyinfra.com 注册后到控制台创建，步骤见 <https://everyinfra.com/docs?utm_source=github&utm_medium=example_repo&utm_campaign=iqiyi-api#quickstart>

### 用 curl 调

```bash
curl -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"platform":"iqiyi","action":"search","params":{"keyword":"纪录片"}}'
```

所有能力都发到同一个地址，换 `action` 和 `params` 就行；`video`、`album` 的写法见 [examples/curl.sh](examples/curl.sh)。

### 接进 Claude、Cursor（MCP）

远程 MCP 地址是 <https://api.everyinfra.com/mcp>，请求头加 `Authorization: Bearer` 和 API Key；服务器由 EveryInfra 运行，不用装本地程序。

Claude Code：

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp --header "Authorization: Bearer <API Key>"
```

Cursor 等读 `mcp.json` 的客户端（[examples/mcp.json](examples/mcp.json)）：

```json
{
  "mcpServers": {
    "everyinfra": {
      "url": "https://api.everyinfra.com/mcp",
      "headers": {
        "Authorization": "Bearer <API Key>"
      }
    }
  }
}
```

Claude 网页版和桌面版的自定义连接器、ChatGPT 只能填网址：填 <https://api.everyinfra.com/mcp/all>，连接时登录 EveryInfra 并允许，不用填 Key。完整步骤见 <https://everyinfra.com/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=iqiyi-api>

### 价格

| 能力 | `action` | 每千次 |
|---|---|---|
| 关键词搜索 | `search` | $1.39 |
| 视频详情 | `video` | $1.39 |
| 专辑 | `album` | $1.39 |

- 按调用次数计费，每次约 $0.0014；失败、空结果、参数错误和鉴权失败都不收费。
- 新账号有 $1 试用额度，24 小时内有效，不用信用卡，领取方式见 <https://everyinfra.com/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=iqiyi-api>

### 返回字段

下面是这 3 个能力实测返回的字段，含义取自接口文档每条说明的第一句，完整说明在每张表下面的链接里。

#### `search`（关键词搜索）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `title` | 标题。 |
| `category` | 分类名称，取值为原平台的分类体系，未做跨平台归一。 |
| `category_id` | 分类 ID。 |
| `duration_seconds` | 时长，单位秒。 |
| `heat_count` | 爱奇艺热度值。 |
| `like_count` | 点赞数。 |
| `comment_count` | 评论数。 |
| `collect_count` | 收藏数。 |
| `image_url` | 图片链接。 |
| `wide_image_url` | 横版海报。 |
| `author_name` | 作者昵称（显示名）。 |
| `author_id` | 作者在原平台的唯一 ID。 |
| `author_avatar_url` | 上传者头像（search / video）。 |
| `author_follower_count` | 作者粉丝数。 |
| `author_video_count` | 作者发布视频数。 |
| `duration_sec` | 时长，单位秒，与 duration_seconds 同值（两个名字都返回）。 |
| `posted_at` | 发布时间，ISO 8601 格式、UTC 时区（如 2026-08-07T12:34:56+00:00）。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `author_location` | 上传者所在地，按页面原文（search / video）。 |
| `author_org` | 认证机构名（机构号用）。 |

完整参数和字段：<https://everyinfra.com/iqiyi-api/search?utm_source=github&utm_medium=example_repo&utm_campaign=iqiyi-api>

#### `video`（视频详情）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `title` | 标题。 |
| `category` | 分类名称，取值为原平台的分类体系，未做跨平台归一。 |
| `category_id` | 分类 ID。 |
| `heat_count` | 爱奇艺热度值。 |
| `like_count` | 点赞数。 |
| `comment_count` | 评论数。 |
| `collect_count` | 收藏数。 |
| `image_url` | 图片链接。 |
| `wide_image_url` | 横版海报。 |
| `author_name` | 作者昵称（显示名）。 |
| `author_id` | 作者在原平台的唯一 ID。 |
| `author_avatar_url` | 上传者头像（search / video）。 |
| `author_follower_count` | 作者粉丝数。 |
| `author_video_count` | 作者发布视频数。 |
| `author_location` | 上传者所在地，按页面原文（search / video）。 |
| `author_org` | 认证机构名（机构号用）。 |
| `posted_at` | 发布时间，ISO 8601 格式、UTC 时区（如 2026-08-07T12:34:56+00:00）。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |

完整参数和字段：<https://everyinfra.com/iqiyi-api/video?utm_source=github&utm_medium=example_repo&utm_campaign=iqiyi-api>

#### `album`（专辑）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `play_url` | 播放页链接。 |
| `title` | 标题。 |
| `type` | 记录类型，取值随能力而定（如 video / image / text）。 |
| `is_series` | 是否为剧集（相对单片）。 |
| `year` | 年份。 |
| `release_date` | 上线日期。 |
| `episode_count` | 集数。 |
| `episode_available_count` | 当前可看集数。 |
| `image_url` | 图片链接。 |
| `episodes` | 分集列表。 |
| `cast` | 演员表。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `subtitle` | 副标题。 |
| `duration_seconds` | 时长，单位秒。 |
| `rating` | 评分。 |
| `content_rating` | 内容分级。 |
| `duration_sec` | 时长，单位秒，与 duration_seconds 同值（两个名字都返回）。 |
| `rating_scale` | 上一列 `rating` 的满分。 |

完整参数和字段：<https://everyinfra.com/iqiyi-api/album?utm_source=github&utm_medium=example_repo&utm_campaign=iqiyi-api>

### 常见问题

**调用时要不要提供爱奇艺账号或 Cookie？**

不用，请求头带 `Authorization: Bearer` 和 API Key 就能调，请求体写 `platform`、`action` 和能力参数。不用扫码、维护登录状态，也不用开浏览器。

**怎么收费？失败了收不收钱？有免费额度吗？**

按调用次数计费，每千次 $1.39 起。失败、空结果、参数错误和鉴权失败都不收费。新账号有 $1 试用额度，24 小时内有效，不用信用卡，领取方式见定价页 <https://everyinfra.com/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=iqiyi-api>

**能把爱奇艺接口接进 Claude、Cursor 吗？**

能，远程 MCP 地址是 <https://api.everyinfra.com/mcp>，请求头加 `Authorization: Bearer` 和 API Key，不用装本地程序。Claude、Cursor、ChatGPT、Claude Code 配置见 <https://everyinfra.com/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=iqiyi-api>。

**用爱奇艺数据要注意哪些合规问题？**

EveryInfra 服务条款要求你自行确保数据用法符合适用法律和相关平台条款，禁止用于违法、侵犯隐私或知识产权，或批量抓取用于骚扰、欺诈等恶意用途。用到昵称、头像等个人信息时，只留业务用得上的字段。

**可以拿到爱奇艺的哪些数据？**

爱奇艺有 3 个能力：关键词搜索、视频详情、专辑。每个能力的参数和返回字段见平台页 <https://everyinfra.com/iqiyi-api?utm_source=github&utm_medium=example_repo&utm_campaign=iqiyi-api>

### 实测记录

发布前用本仓的代码对线上接口跑过一遍，命令就是「快速开始」里的 3 条。

| 命令 | 时间（新加坡时间） | 返回条数 | 扣费 |
|---|---|---|---|
| `python main.py search 纪录片 --out videos.csv` | 2026-11-21 09:37 | 20 | $0.001389 |
| `python main.py video "<视频链接>" --out video.json` | 2026-11-21 09:38 | 1 | $0.001389 |
| `python main.py album 苍兰诀 --out album.json` | 2026-11-21 09:43 | 10 | $0.001389 |

`video` 返回的一条（正文截到 60 字，作者字段没放进来）：

```json
{
  "id": "2634814001270900",
  "title": " 荒野独居第十四季-2 #荒野求生 #纪录片 #生存",
  "category": "纪录片",
  "heat_count": 250,
  "like_count": 1,
  "comment_count": 0,
  "collect_count": 1,
  "posted_at": "2026-11-20T14:05:00+00:00"
}
```

## License

MIT

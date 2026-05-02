import os, re, glob, json

# ============================================================
# 网站重构 v3 - 学术清爽风
# ============================================================

# ---- 收集博客数据 ----
blogs = []
for f in sorted(glob.glob('blog/*.html')):
    name = os.path.basename(f)
    nl = name.lower()
    tags = []
    if any(k in nl for k in ['vln','nav','cow','fscot','stop','cot','haltnav','evolvenav','fantasyvla','acot','calibration','rule-vln','sim2real','cross-modal','confidence','reasoning','live','lazy','safenav','navcot','navdp','dreamnav','spatialmem','bev','slam','embodied-splat']):
        tags.append('研究笔记')
    if any(k in nl for k in ['startup','funding','capital','investment','valuation','ipo','bubble','crisis','market','commercial','business','hardware','vertical','death','survival','robot-ipo']):
        tags.append('创业思考')
    if any(k in nl for k in ['vla','embodied-ai-2026','embodied-ai-apr','embodied-ai-300','embodied-intelligence','frontier','world-model','cvpr','iclr','deep-review','paradigm','five-paradigms','worldarena','physical-grounding','dm0','reasoning-chain','vla-era','robot-recent']):
        tags.append('热点观察')
    if not tags:
        tags.append('日记')
    
    title = name.replace('.html','').replace('-',' ').title()
    blogs.append({"name": name, "url": "./blog/" + name, "tags": tags, "title": title})

# ---- 收集案例数据 ----
cases = []
for f in sorted(glob.glob('cases/*.md')):
    name = os.path.basename(f)
    title = name.replace('.md','').replace('-',' ').title()
    cases.append({"name": name, "url": "./cases/" + name, "tags": ["创业思考"], "title": title})

# ---- 论文数据 ----
papers = [
    {"id":"cow-nav","title":"CoW-Nav: Confidence-Weighted Navigation with Formally Structured Chain of Thought","authors":"Jingwei013","venue":"ICRA 2027 / RAL","year":2027,"type":"mine","status":"writing","abstract":"FSCoT稀疏思维链+信心头双头架构，解决VLN停止决策问题","tags":["CoW-Nav","stop-decision","FSCoT"],"progress":20},
    {"id":"embodied-slam","title":"EmbodiedSLAM: Tri-Modal Fusion for Embodied Navigation","authors":"Jingwei013","venue":"ICRA 2027","year":2026,"type":"mine","status":"planning","abstract":"视觉里程计+语言先验+语义地图三模态融合","tags":["SLAM","tri-modal"],"progress":5},
    {"id":"haltnav-pro","title":"HaltNav-Pro: Adaptive Threshold Stopping for VLN","authors":"Various","venue":"ICRA 2025","year":2025,"type":"ref","abstract":"自适应阈值停止，R2R StoP +3.2%","tags":["stop-decision","VLN"]},
    {"id":"evolvnav-2","title":"EvolveNav-2: Online CoT Self-Improvement for VLN","authors":"Various","venue":"ICRA 2025","year":2025,"type":"ref","abstract":"在线CoT自改进，长距离SR +5.1%","tags":["CoT","VLN"]},
    {"id":"vlr1","title":"VLN-R1: RLHF with Chain-of-Thought for VLN","authors":"Various","venue":"arXiv 2026","year":2026,"type":"ref","abstract":"RLHF+CoT，探索性工作","tags":["VLN","RLHF","CoT"]},
    {"id":"fantasyvla","title":"FantasyVLA: Fast CoT for Vision-Language-Action","authors":"Various","venue":"CVPR 2026","year":2026,"type":"ref","abstract":"快速CoT方法，对比FSCoT的重要参考","tags":["VLA","CoT"]},
    {"id":"acot-vla","title":"ACoT-VLA: Action Chain-of-Thought for VLA Models","authors":"Various","venue":"CVPR 2026","year":2026,"type":"ref","abstract":"动作链思维，停止决策参考","tags":["VLA","action-CoT"]},
    {"id":"vl-calibration","title":"VL-Calibration: VLM Confidence Calibration for VLN","authors":"Various","venue":"ICLR 2026","year":2026,"type":"ref","abstract":"VLM置信度校准，直接关联信心头设计","tags":["calibration","confidence"]},
    {"id":"rule-vln","title":"Rule-VLN: Social Compliance for VLN","authors":"Various","venue":"arXiv 2026","year":2026,"type":"ref","abstract":"社会合规VLN，CVR指标与双头扩展相关","tags":["VLN","social-compliance"]},
    {"id":"vla-nav","title":"VLA-Nav: End-to-End VLA Navigation without Fine-tuning","authors":"Various","venue":"arXiv 2026","year":2026,"type":"ref","abstract":"零样本VLA导航","tags":["VLA","zero-shot"]},
    {"id":"navdp","title":"NavDP: Depth-Progressive Planning for VLN","authors":"Various","venue":"ICRA 2026","year":2026,"type":"ref","abstract":"深度递进规划，分层决策参考","tags":["VLN","planning"]},
    {"id":"dreamnav","title":"DreamNav: World Model Predictive Planning for VLN","authors":"Various","venue":"ICRA 2026","year":2026,"type":"ref","abstract":"世界模型预测规划","tags":["world-model","VLN"]},
    {"id":"univ3r","title":"Uni3R: Unified 3D Reasoning for Embodied AI","authors":"Various","venue":"CVPR 2026","year":2026,"type":"ref","abstract":"统一3D推理，与EmbodiedSLAM直接相关","tags":["3D-reasoning","perception"]},
    {"id":"safevla","title":"SafeVLA: Safe Vision-Language-Action Models","authors":"Various","venue":"ICRA 2026","year":2026,"type":"ref","abstract":"安全VLA模型+WorldArena评测","tags":["VLA","safety"]},
    {"id":"navspace","title":"NavSpace: Spatial Intelligence Benchmark for VLN","authors":"Various","venue":"arXiv 2026","year":2026,"type":"ref","abstract":"空间智能评测，可扩展FSCoT四段式推理","tags":["benchmark","spatial"]},
    {"id":"pi0","title":"\u03c00: Physical Intelligence Generalist Robot Model","authors":"Physical Intelligence","venue":"2024","year":2024,"type":"ref","abstract":"24亿美元估值VLA基础模型","tags":["VLA","robotics"]},
]

# ---- 生成HTML ----
blogs_json = json.dumps(blogs, ensure_ascii=False, indent=0)
cases_json = json.dumps(cases, ensure_ascii=False, indent=0)
papers_json = json.dumps(papers, ensure_ascii=False, indent=0)

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>\u7cbe\u536b\u5bfc\u822a | \u5177\u8eab\u667a\u80fd\u7814\u7a76\u8005</title>
  <meta name="description" content="\u7cbe\u536b\u5bfc\u822a - \u5177\u8eab\u667a\u80fd\u3001\u89c6\u89c9\u8bed\u8a00\u5bfc\u822a(VLN)\u3001\u4e16\u754c\u6a21\u578b\u7814\u7a76\u65b9\u5411\u7684\u4e2a\u4eba\u7f51\u7ad9">
  <style>
    :root {{
      --navy: #1a2744;
      --navy-light: #2d3e5e;
      --orange: #e07b39;
      --orange-light: #f0a060;
      --teal: #2a9d8f;
      --bg: #fafafa;
      --bg-card: #ffffff;
      --text: #1a1a2e;
      --text2: #4a4a6a;
      --text3: #8888aa;
      --border: #e8e8ee;
      --shadow: 0 1px 3px rgba(0,0,0,0.06);
      --radius: 8px;
    }}
    * {{ margin:0; padding:0; box-sizing:border-box; }}
    body {{
      font-family: -apple-system, 'Segoe UI', 'Noto Sans SC', sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.7;
    }}
    a {{ color: var(--teal); text-decoration: none; }}
    a:hover {{ color: var(--orange); }}

    /* === NAV === */
    nav {{
      background: var(--navy);
      position: sticky; top:0; z-index:100;
    }}
    nav .inner {{
      max-width: 960px; margin:0 auto; padding:0 24px;
      display:flex; align-items:center; height:56px; gap:32px;
    }}
    nav .brand {{
      color:#fff; font-weight:700; font-size:18px; white-space:nowrap;
      display:flex; align-items:center; gap:8px;
    }}
    nav .brand span {{
      width:28px; height:28px; border-radius:50%;
      background: var(--orange); display:flex; align-items:center; justify-content:center;
      font-size:14px; font-weight:800;
    }}
    nav ul {{ display:flex; gap:4px; list-style:none; }}
    nav a {{
      color:rgba(255,255,255,0.7); padding:6px 14px; border-radius:6px;
      font-size:14px; font-weight:500; transition: all .15s;
    }}
    nav a:hover, nav a.active {{
      color:#fff; background:rgba(255,255,255,0.12);
    }}

    /* === LAYOUT === */
    .page {{ max-width:960px; margin:0 auto; padding:40px 24px 80px; }}
    .hidden {{ display:none !important; }}

    /* === HOME === */
    .hero {{
      background: linear-gradient(135deg, var(--navy) 0%, var(--navy-light) 100%);
      color:#fff; padding:60px 24px; text-align:center;
    }}
    .hero h1 {{ font-size:36px; font-weight:800; margin-bottom:8px; letter-spacing:-0.5px; }}
    .hero .sub {{ font-size:16px; opacity:.8; margin-bottom:32px; }}
    .hero-stats {{
      display:flex; justify-content:center; gap:40px;
    }}
    .hero-stat-num {{ font-size:32px; font-weight:700; color:var(--orange); }}
    .hero-stat-label {{ font-size:12px; opacity:.6; }}

    .section-title {{
      font-size:22px; font-weight:700; color:var(--navy);
      margin-bottom:20px; padding-bottom:8px;
      border-bottom:2px solid var(--orange);
      display:inline-block;
    }}

    /* Research cards */
    .research-grid {{
      display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-bottom:48px;
    }}
    .r-card {{
      background:var(--bg-card); border-radius:var(--radius); padding:20px;
      border:1px solid var(--border); border-left:3px solid var(--orange);
      transition: box-shadow .15s;
    }}
    .r-card:hover {{ box-shadow: 0 4px 12px rgba(0,0,0,0.08); }}
    .r-card h3 {{ font-size:15px; color:var(--navy); margin-bottom:6px; }}
    .r-card p {{ font-size:13px; color:var(--text2); }}
    .r-card .progress-bar {{
      margin-top:10px; height:4px; background:var(--border); border-radius:2px;
    }}
    .r-card .progress-fill {{
      height:100%; background:var(--orange); border-radius:2px;
    }}
    .r-card .progress-label {{ font-size:11px; color:var(--text3); margin-top:4px; }}

    /* Blog preview */
    .blog-preview-item {{
      padding:12px 0; border-bottom:1px solid var(--border);
      display:flex; justify-content:space-between; align-items:baseline;
    }}
    .blog-preview-item:last-child {{ border-bottom:none; }}
    .blog-preview-item a {{ font-size:14px; color:var(--text); }}
    .blog-preview-item a:hover {{ color:var(--orange); }}
    .blog-preview-item .date {{ font-size:12px; color:var(--text3); white-space:nowrap; }}

    /* === PAPERS (Timeline) === */
    .paper-filters {{
      display:flex; gap:8px; margin-bottom:24px; flex-wrap:wrap;
    }}
    .paper-filters button {{
      padding:6px 14px; border-radius:20px; border:1px solid var(--border);
      background:var(--bg-card); font-size:13px; cursor:pointer;
      color:var(--text2); transition: all .15s;
    }}
    .paper-filters button:hover {{ border-color:var(--teal); }}
    .paper-filters button.active {{
      background:var(--navy); color:#fff; border-color:var(--navy);
    }}

    .timeline {{ position:relative; padding-left:32px; }}
    .timeline::before {{
      content:''; position:absolute; left:8px; top:0; bottom:0;
      width:2px; background:var(--border);
    }}
    .timeline-year {{
      position:relative; margin-bottom:24px;
    }}
    .timeline-year .year-label {{
      position:absolute; left:-32px; top:0;
      width:18px; height:18px; border-radius:50%;
      background:var(--navy); border:3px solid var(--bg);
    }}
    .timeline-year h3 {{
      font-size:18px; color:var(--navy); margin-bottom:12px;
      padding-left:8px;
    }}
    .paper-card {{
      background:var(--bg-card); border-radius:var(--radius);
      padding:16px; margin-bottom:10px; margin-left:8px;
      border:1px solid var(--border); transition: box-shadow .15s;
    }}
    .paper-card:hover {{ box-shadow:0 2px 8px rgba(0,0,0,0.06); }}
    .paper-card.mine {{
      border-left:3px solid var(--orange);
      background: linear-gradient(90deg, #fff8f0 0%, #fff 30%);
    }}
    .paper-card.ref {{
      border-left:3px solid var(--teal);
    }}
    .paper-card .venue {{
      font-size:11px; color:var(--orange); font-weight:600;
      text-transform:uppercase; margin-bottom:4px;
    }}
    .paper-card.ref .venue {{ color:var(--teal); }}
    .paper-card .title {{ font-size:14px; font-weight:600; color:var(--text); margin-bottom:4px; }}
    .paper-card .authors {{ font-size:12px; color:var(--text3); margin-bottom:4px; }}
    .paper-card .abstract {{ font-size:12px; color:var(--text2); line-height:1.5; }}
    .paper-card .tags {{ display:flex; gap:4px; margin-top:8px; flex-wrap:wrap; }}
    .paper-card .tag {{
      font-size:10px; padding:2px 8px; border-radius:10px;
      background:var(--bg); color:var(--text3); border:1px solid var(--border);
    }}

    /* === BLOG === */
    .blog-filters {{
      display:flex; gap:8px; margin-bottom:20px; flex-wrap:wrap;
    }}
    .blog-filters button {{
      padding:6px 14px; border-radius:20px; border:1px solid var(--border);
      background:var(--bg-card); font-size:13px; cursor:pointer;
      color:var(--text2); transition: all .15s;
    }}
    .blog-filters button:hover {{ border-color:var(--teal); }}
    .blog-filters button.active {{
      background:var(--navy); color:#fff; border-color:var(--navy);
    }}
    .blog-list {{ }}
    .blog-item {{
      padding:14px 0; border-bottom:1px solid var(--border);
      display:flex; gap:12px; align-items:baseline;
    }}
    .blog-item .tag-pill {{
      font-size:11px; padding:2px 8px; border-radius:10px;
      white-space:nowrap; font-weight:500;
    }}
    .blog-item .tag-pill.research {{ background:#e8f4f8; color:#2a9d8f; }}
    .blog-item .tag-pill.startup {{ background:#fff4e8; color:#e07b39; }}
    .blog-item .tag-pill.hot {{ background:#f0e8ff; color:#6a4cc8; }}
    .blog-item .tag-pill.diary {{ background:#f0f0f0; color:#666; }}
    .blog-item a {{ font-size:14px; color:var(--text); flex:1; }}
    .blog-item a:hover {{ color:var(--orange); }}

    /* === ABOUT === */
    .about-content {{ max-width:640px; }}
    .about-content h3 {{ color:var(--navy); margin:24px 0 8px; font-size:16px; }}
    .about-content p {{ font-size:14px; color:var(--text2); margin-bottom:12px; }}

    /* === FOOTER === */
    footer {{
      text-align:center; padding:24px; font-size:12px; color:var(--text3);
      border-top:1px solid var(--border);
    }}

    /* === RESPONSIVE === */
    @media (max-width:640px) {{
      .hero h1 {{ font-size:28px; }}
      .hero-stats {{ gap:20px; }}
      .hero-stat-num {{ font-size:24px; }}
      .research-grid {{ grid-template-columns:1fr; }}
      nav ul {{ gap:0; }}
      nav a {{ padding:6px 10px; font-size:13px; }}
    }}
  </style>
</head>
<body>

<nav>
  <div class="inner">
    <div class="brand"><span>\u7cbe</span> \u7cbe\u536b\u5bfc\u822a</div>
    <ul>
      <li><a href="#" onclick="show('home');return false" class="active" data-nav="home">\u9996\u9875</a></li>
      <li><a href="#" onclick="show('papers');return false" data-nav="papers">\u8bba\u6587</a></li>
      <li><a href="#" onclick="show('blog');return false" data-nav="blog">\u535a\u5ba2</a></li>
      <li><a href="#" onclick="show('about');return false" data-nav="about">\u5173\u4e8e</a></li>
    </ul>
  </div>
</nav>

<!-- ===== HOME ===== -->
<section id="home">
  <div class="hero">
    <h1>\u7cbe\u536b\u5bfc\u822a</h1>
    <p class="sub">\u5177\u8eab\u667a\u80fd\u7814\u7a76\u8005 \u00b7 \u89c6\u89c9\u8bed\u8a00\u5bfc\u822a(VLN) \u00b7 \u535a\u58eb\u7814\u7a76\u751f</p>
    <div class="hero-stats">
      <div><div class="hero-stat-num">2</div><div class="hero-stat-label">\u5728\u7814\u8bba\u6587</div></div>
      <div><div class="hero-stat-num">{len(papers)}</div><div class="hero-stat-label">\u53c2\u8003\u6587\u732e</div></div>
      <div><div class="hero-stat-num">{len(blogs)+len(cases)}</div><div class="hero-stat-label">\u535a\u5ba2</div></div>
    </div>
  </div>
  <div class="page">
    <h2 class="section-title">\u7814\u7a76\u65b9\u5411</h2>
    <div class="research-grid">
      <div class="r-card">
        <h3>CoW-Nav \u505c\u6b62\u51b3\u7b56</h3>
        <p>FSCoT\u7a00\u758f\u601d\u7ef4\u94fe + \u4fe1\u5fc3\u5934\u53cc\u5934\u67b6\u6784\uff0c\u89e3\u51b3VLN\u201c\u8be5\u505c\u4e0d\u505c\u201d\u95ee\u9898</p>
        <div class="progress-bar"><div class="progress-fill" style="width:20%"></div></div>
        <div class="progress-label">\u8fdb\u5ea6 20% \u00b7 \u76ee\u6807 ICRA 2027 / RAL</div>
      </div>
      <div class="r-card">
        <h3>EmbodiedSLAM</h3>
        <p>\u89c6\u89c9\u91cc\u7a0b\u8ba1 + \u8bed\u8a00\u5148\u9a8c + \u8bed\u4e49\u5730\u56fe\u4e09\u6a21\u6001\u878d\u5408</p>
        <div class="progress-bar"><div class="progress-fill" style="width:5%"></div></div>
        <div class="progress-label">\u8fdb\u5ea6 5% \u00b7 \u89c4\u5212\u4e2d</div>
      </div>
      <div class="r-card">
        <h3>\u4e16\u754c\u6a21\u578b\u5bfc\u822a</h3>
        <p>\u5229\u7528\u4e16\u754c\u6a21\u578b\u9884\u6d4b\u672a\u6765\u72b6\u6001\uff0c\u5b9e\u73b0\u6837\u672c\u9ad8\u6548\u5f3a\u5316\u5b66\u4e60\u5bfc\u822a</p>
        <div class="progress-bar"><div class="progress-fill" style="width:10%"></div></div>
        <div class="progress-label">\u8fdb\u5ea6 10% \u00b7 \u6587\u732e\u8c03\u7814\u4e2d</div>
      </div>
      <div class="r-card">
        <h3>VLA \u57fa\u7840\u6a21\u578b</h3>
        <p>Vision-Language-Action\u6a21\u578b\u5728\u5177\u8eab\u667a\u80fd\u4e2d\u7684\u5e94\u7528\u4e0e\u5fae\u8c03\u7b56\u7565</p>
        <div class="progress-bar"><div class="progress-fill" style="width:8%"></div></div>
        <div class="progress-label">\u8fdb\u5ea6 8% \u00b7 \u524d\u671f\u63a2\u7d22</div>
      </div>
    </div>

    <h2 class="section-title">\u6700\u65b0\u535a\u5ba2</h2>
    <div id="homeBlogs"></div>
    <div style="margin-top:16px">
      <a href="#" onclick="show('blog');return false" style="font-size:14px">\u67e5\u770b\u5168\u90e8\u535a\u5ba2 \u2192</a>
    </div>
  </div>
</section>

<!-- ===== PAPERS ===== -->
<section id="papers" class="hidden">
  <div class="page">
    <h2 class="section-title">\u8bba\u6587\u65f6\u95f4\u7ebf</h2>
    <p style="color:var(--text2);font-size:14px;margin-bottom:20px">\u53c2\u8003\u6587\u732e\u5e93\uff0c\u4e3a\u7814\u7a76\u670d\u52a1</p>
    <div class="paper-filters">
      <button onclick="filterPapers('all')" class="active">\u5168\u90e8</button>
      <button onclick="filterPapers('mine')">\u6211\u7684\u8bba\u6587</button>
      <button onclick="filterPapers('ref')">\u53c2\u8003\u6587\u732e</button>
    </div>
    <div class="timeline" id="papersTimeline"></div>
  </div>
</section>

<!-- ===== BLOG ===== -->
<section id="blog" class="hidden">
  <div class="page">
    <h2 class="section-title">\u535a\u5ba2</h2>
    <p style="color:var(--text2);font-size:14px;margin-bottom:20px">\u7814\u7a76\u7b14\u8bb0\u3001\u70ed\u70b9\u89c2\u5bdf\u3001\u601d\u8003\u65e5\u8bb0</p>
    <div class="blog-filters">
      <button onclick="filterBlog('all')" class="active">\u5168\u90e8</button>
      <button onclick="filterBlog('\u7814\u7a76\u7b14\u8bb0')">\u7814\u7a76\u7b14\u8bb0</button>
      <button onclick="filterBlog('\u521b\u4e1a\u601d\u8003')">\u521b\u4e1a\u601d\u8003</button>
      <button onclick="filterBlog('\u70ed\u70b9\u89c2\u5bdf')">\u70ed\u70b9\u89c2\u5bdf</button>
      <button onclick="filterBlog('\u65e5\u8bb0')">\u65e5\u8bb0</button>
    </div>
    <div class="blog-list" id="blogList"></div>
  </div>
</section>

<!-- ===== ABOUT ===== -->
<section id="about" class="hidden">
  <div class="page">
    <h2 class="section-title">\u5173\u4e8e</h2>
    <div class="about-content">
      <h3>\u7cbe\u536b013</h3>
      <p>\u535a\u58eb\u7814\u7a76\u751f\uff0c\u5177\u8eab\u667a\u80fd/\u89c6\u89c9\u8bed\u8a00\u5bfc\u822a\u65b9\u5411\u3002\u7814\u7a76\u76ee\u6807\uff1a\u53d1\u8868SCI\u8bba\u6587\uff08ICRA 2027 / RAL / IROS 2026\uff09\u3002</p>

      <h3>\u535a\u58eb\u8bba\u6587</h3>
      <p>\u300a\u9762\u5411\u5177\u8eab\u667a\u80fd\u4f53\u7684\u81ea\u4e3b\u611f\u77e5\u3001\u51b3\u7b56\u4e0e\u5bfc\u822a\u5173\u952e\u6280\u672f\u7814\u7a76\u300b</p>

      <h3>\u7814\u7a76\u57fa\u91d1</h3>
      <p>\u5317\u4eac\u5e02\u81ea\u7136\u79d1\u5b66\u57fa\u91d1-\u4e30\u53f0\u521b\u65b0\u8054\u5408\u57fa\u91d1\uff0c100\u4e07\uff0c2024.10-2027.9\u3002\u627f\u62c5\u8bfe\u9898\u4e09\u00a72.3\u8de8\u573a\u666f\u5bfc\u822a\u5b9a\u4f4d\u4e0e\u8def\u5f84\u89c4\u5212\u3002</p>

      <h3>\u8054\u7cfb</h3>
      <p>GitHub: <a href="https://github.com/Jingwei013" target="_blank">Jingwei013</a></p>
      <p>\u7f51\u7ad9: <a href="https://jingwei013.github.io" target="_blank">jingwei013.github.io</a></p>
    </div>
  </div>
</section>

<footer>
  \u00a9 2026 \u7cbe\u536b013 \u00b7 \u5177\u8eab\u667a\u80fd\u4e0e\u5bfc\u822a\u7814\u7a76
</footer>

<script>
const PAPERS = {papers_json};
const BLOGS = {blogs_json};
const CASES = {cases_json};

// --- Navigation ---
function show(id) {{
  document.querySelectorAll('section').forEach(s => s.classList.add('hidden'));
  document.getElementById(id).classList.remove('hidden');
  document.querySelectorAll('nav a').forEach(a => a.classList.remove('active'));
  const navA = document.querySelector('nav a[data-nav="'+id+'"]');
  if (navA) navA.classList.add('active');
  window.scrollTo(0, 0);
}}

// --- Home: latest blogs ---
function renderHomeBlogs() {{
  const el = document.getElementById('homeBlogs');
  const all = [...BLOGS, ...CASES];
  // Show latest 8
  let html = '';
  for (let i = 0; i < Math.min(8, all.length); i++) {{
    const b = all[all.length - 1 - i];
    html += '<div class="blog-preview-item"><a href="'+b.url+'">'+b.title+'</a></div>';
  }}
  el.innerHTML = html;
}}

// --- Papers: Timeline ---
let paperFilter = 'all';
function filterPapers(type) {{
  paperFilter = type;
  document.querySelectorAll('.paper-filters button').forEach(b => b.classList.remove('active'));
  event.target.classList.add('active');
  renderPapers();
}}

function renderPapers() {{
  const el = document.getElementById('papersTimeline');
  let filtered = PAPERS;
  if (paperFilter !== 'all') filtered = PAPERS.filter(p => p.type === paperFilter);

  // Group by year
  const years = {{}};
  filtered.forEach(p => {{
    if (!years[p.year]) years[p.year] = [];
    years[p.year].push(p);
  }});

  let html = '';
  Object.keys(years).sort((a,b) => b-a).forEach(year => {{
    html += '<div class="timeline-year">';
    html += '<div class="year-label"></div>';
    html += '<h3>' + year + '</h3>';
    years[year].forEach(p => {{
      const cls = p.type === 'mine' ? 'mine' : 'ref';
      const icon = p.type === 'mine' ? '[My] ' : '';
      const statusBadge = p.status ? ' <span style="font-size:11px;color:var(--orange);font-weight:600">' + p.status + '</span>' : '';
      html += '<div class="paper-card ' + cls + '">';
      html += '<div class="venue">' + p.venue + '</div>';
      html += '<div class="title">' + icon + p.title + statusBadge + '</div>';
      html += '<div class="authors">' + p.authors + '</div>';
      if (p.abstract) html += '<div class="abstract">' + p.abstract + '</div>';
      if (p.tags) {{
        html += '<div class="tags">';
        p.tags.forEach(t => html += '<span class="tag">' + t + '</span>');
        html += '</div>';
      }}
      html += '</div>';
    }});
    html += '</div>';
  }});
  el.innerHTML = html;
}}

// --- Blog: List ---
let blogFilter = 'all';
function filterBlog(tag) {{
  blogFilter = tag;
  document.querySelectorAll('.blog-filters button').forEach(b => b.classList.remove('active'));
  event.target.classList.add('active');
  renderBlog();
}}

function renderBlog() {{
  const el = document.getElementById('blogList');
  let all = [...BLOGS, ...CASES];
  if (blogFilter !== 'all') {{
    all = all.filter(b => b.tags && b.tags.includes(blogFilter));
  }}

  let html = '';
  all.forEach(b => {{
    const tagClass = b.tags && b.tags[0] ? b.tags[0] : 'diary';
    const cls = tagClass === '\u7814\u7a76\u7b14\u8bb0' ? 'research'
              : tagClass === '\u521b\u4e1a\u601d\u8003' ? 'startup'
              : tagClass === '\u70ed\u70b9\u89c2\u5bdf' ? 'hot' : 'diary';
    html += '<div class="blog-item">';
    html += '<span class="tag-pill ' + cls + '">' + (b.tags ? b.tags[0] : '\u65e5\u8bb0') + '</span>';
    html += '<a href="' + b.url + '">' + b.title + '</a>';
    html += '</div>';
  }});
  el.innerHTML = html;
}}

// --- Init ---
document.addEventListener('DOMContentLoaded', function() {{
  renderHomeBlogs();
  renderPapers();
  renderBlog();
}});
</script>
</body>
</html>'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"index.html written: {len(html)} bytes")
print(f"Papers: {len(papers)}, Blogs: {len(blogs)}, Cases: {len(cases)}")

# Verify UTF-8
with open('index.html', 'rb') as f:
    raw = f.read()
raw.decode('utf-8')  # Will throw if invalid
print("UTF-8 validation: OK")

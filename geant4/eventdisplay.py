"""Event display for the Geant4 tutorial notebooks (tutorial.ipynb, macros.ipynb).

Import it after run_g4.C has been run:

    ROOT.gROOT.ProcessLine('.x run_g4.C(false)')
    from eventdisplay import event_gui, print_tracks, show3d, run_macro

event_gui(app)       particle/momentum controls, "Next event" button and the event view
print_tracks(pmin)   table of the tracks of the last event
show3d(pmin)         interactive 3D view (JSROOT) of the last event
run_macro('dEdx.C')  run an analysis macro, showing events and histograms while it runs
"""
import json as json_module
import os
import tempfile
import uuid

import ROOT
import ipywidgets as widgets
from IPython.display import HTML, Image, display

try:
    _App = ROOT.TutorialApplication
except AttributeError:
    raise ImportError("run ROOT.gROOT.ProcessLine('.x run_g4.C(false)') before importing eventdisplay")

# track colours by particle type (other particles: grey)
TRACK_COLORS = {11: ROOT.kRed, -11: ROOT.kBlue, 22: ROOT.kGreen + 2,
                13: ROOT.kMagenta, -13: ROOT.kMagenta, 211: ROOT.kOrange + 7,
                -211: ROOT.kOrange + 7, 111: ROOT.kOrange, 2212: ROOT.kCyan + 2,
                -2212: ROOT.kCyan + 2, 2112: ROOT.kGray + 2}

PARTICLES = [('e-', 11), ('e+', -11), ('mu-', 13), ('mu+', -13), ('gamma', 22),
             ('pi+', 211), ('pi0', 111), ('pi-', -211), ('p', 2212),
             ('anti-p', -2212), ('n', 2112)]


# --- no automatic notebook output from InitMC/RunMC -------------------------
# ROOT's notebook integration shows, after each cell, every canvas that was
# updated and the last drawn geometry. Here these views would show the detector
# without tracks; the event display below replaces them.

def _quiet(app):
    pad = app.GetDrawPad()
    if pad:
        canvas = pad.GetCanvas()
        canvas.ResetDrawn()
        canvas.ResetUpdated()
    if ROOT.gGeoManager:
        ROOT.gGeoManager.SetUserPaintVolume(ROOT.nullptr)


if not getattr(_App, '_eventdisplay_quiet', False):
    _InitMC, _RunMC = _App.InitMC, _App.RunMC

    def InitMC(self, *args):
        result = _InitMC(self, *args)
        _quiet(self)
        return result

    def RunMC(self, *args):
        result = _RunMC(self, *args)
        _quiet(self)
        return result

    _App.InitMC, _App.RunMC = InitMC, RunMC
    _App._eventdisplay_quiet = True


# --- tracks of the last event ---------------------------------------------

def track_table(pmin=0.0):
    """all tracks of the last event: (id, mother, particle, pdg, p [GeV], px, py, pz)"""
    rows = []
    geo = ROOT.gGeoManager
    for i in range(geo.GetNtracks()):
        trk = geo.GetTrack(i)
        p = trk.GetParticle()               # TParticle at creation of the track
        if p.P() >= pmin:
            rows.append((trk.GetId(), p.GetFirstMother(), p.GetName(), p.GetPdgCode(),
                         p.P(), p.Px(), p.Py(), p.Pz()))
    return rows


def print_tracks(pmin=0.0):
    """print the tracks of the last event with momentum >= pmin (GeV)"""
    print(f"{'id':>4} {'mother':>6}  {'particle':10} {'pdg':>6} {'p [GeV]':>10}"
          f" {'px':>9} {'py':>9} {'pz':>9}")
    for r in track_table(pmin):
        print(f"{r[0]:4d} {r[1]:6d}  {r[2]:10} {r[3]:6d} {r[4]:10.4g}"
              f" {r[5]:9.3g} {r[6]:9.3g} {r[7]:9.3g}")


def color_tracks():
    """colour the tracks by particle type (TRACK_COLORS)"""
    geo = ROOT.gGeoManager
    for i in range(geo.GetNtracks()):
        trk = geo.GetTrack(i)
        trk.SetLineColor(TRACK_COLORS.get(trk.GetPDG(), ROOT.kGray + 1))


# --- 3D view (JSROOT) -----------------------------------------------------

# compact JSON of the tracks: points per track, colour, tooltip label and the
# points (cm, 0.01 mm precision). Much smaller than the ROOT objects
# (a 20 GeV shower has >10000 tracks).
if not hasattr(ROOT, 'g4_tracks_json'):
    ROOT.gInterpreter.Declare(r'''
#include <string>
#include "TGeoManager.h"
#include "TVirtualGeoTrack.h"
#include "TParticle.h"
#include "TString.h"
std::string g4_tracks_json(double pmin) {
   std::string n, c, l, p;
   for (Int_t i = 0; i < gGeoManager->GetNtracks(); ++i) {
      TVirtualGeoTrack *trk = gGeoManager->GetTrack(i);
      TParticle *part = (TParticle *)trk->GetParticle();
      if (!part || trk->GetNpoints() < 2 || part->P() < pmin)
         continue;
      if (!n.empty()) { n += ','; c += ','; l += ','; }
      n += std::to_string(trk->GetNpoints());
      c += std::to_string(trk->GetLineColor());
      l += TString::Format("\"%s  id %d  mother %d  p = %.4g GeV\"", part->GetName(),
                           trk->GetId(), part->GetFirstMother(), part->P()).Data();
      for (Int_t k = 0; k < trk->GetNpoints(); ++k) {
         const Double_t *x = trk->GetPoint(k);
         p += TString::Format(p.empty() ? "%.3f,%.3f,%.3f" : ",%.3f,%.3f,%.3f", x[0], x[1], x[2]).Data();
      }
   }
   return "{\"n\":[" + n + "],\"c\":[" + c + "],\"l\":[" + l + "],\"p\":[" + p + "]}";
}
''')


def _zip(json):
    """JS expression giving a promise of the JSON text; compressed when possible
       (ROOT's zipJSON handles at most 16 MB)"""
    z = str(ROOT.TBufferJSON.zipJSON(json))
    if z:
        return f"Core.unzipJSON({len(json)}, '{z}')"
    return "Promise.resolve(" + json_module.dumps(json) + ")"


def display3d_html(pmin=0.0, width=700, height=700, view=None):
    """HTML: geometry + tracks of the last event in JSROOT.
       Hover over a track shows particle, track id and momentum.
       Views with the same `view` name share the camera: a new event is shown
       with the orientation and zoom of the previous one."""
    color_tracks()
    geo = ROOT.gGeoManager
    jgeo = str(ROOT.TBufferJSON.ToJSON(geo.GetTopVolume(), 23))
    jtrk = str(ROOT.g4_tracks_json(pmin))
    div = 'g4disp_' + uuid.uuid4().hex
    # JSROOT loading as in ROOT's own notebook display (JupyROOT), incl. require.js
    return f"""
<div id="{div}" style="width:{width}px; height:{height}px; position:relative"></div>
<script>
(function() {{
   function fail(err) {{
      const el = document.getElementById('{div}');
      if (el) el.textContent = 'event display failed: ' + err;
   }}
   const key = {json_module.dumps(view)};
   function save(p) {{
      // remember the camera of this view (kind, position, zoom, target)
      const cam = p.getCamera?.(), ctrl = p.getControls?.();
      if (!key || !cam || !ctrl?.target) return;
      (window.g4_views ??= {{}})[key] = {{
         kind: p.ctrl.camera_kind, overlay: p.ctrl.camera_overlay, zoom: cam.zoom,
         pos: cam.position.toArray(), up: cam.up.toArray(), target: ctrl.target.toArray() }};
   }}
   function restore(p) {{
      const s = key && window.g4_views?.[key];
      if (!s) return;
      if (s.kind !== p.ctrl.camera_kind || s.overlay !== p.ctrl.camera_overlay) {{
         p.ctrl.camera_kind = s.kind;
         p.ctrl.camera_overlay = s.overlay;
         p.changeCamera();
      }}
      const cam = p.getCamera(), ctrl = p.getControls();
      cam.position.fromArray(s.pos);
      cam.up.fromArray(s.up);
      cam.zoom = s.zoom;
      cam.updateProjectionMatrix();
      ctrl.target.fromArray(s.target);
      cam.lookAt(ctrl.target);
      ctrl.update?.();
      p.render3D(0);
   }}
   function sharpen(p) {{
      // hovering picks the track nearest to the mouse, within a few pixels
      // (JSROOT default: anything within 10 cm), and prefers tracks over volumes
      if (!p.g4_camera_hook) {{
         // a camera change from the menu recreates the controls: patch them again
         p.g4_camera_hook = true;
         const change = p.changeCamera;
         p.changeCamera = function(...args) {{
            const res = change.apply(this, args);
            sharpen(this);
            return res;
         }};
      }}
      const ctrl = p.getControls?.();
      if (!ctrl || ctrl.g4_sharp) return;
      ctrl.g4_sharp = true;
      ctrl.addEventListener?.('change', () => save(p));
      const orig = ctrl.getMouseIntersects;
      ctrl.getMouseIntersects = function(mouse) {{
         const cam = this.camera, h = this.renderer.domElement.clientHeight || 500,
               cm_per_pixel = cam.isOrthographicCamera ? (cam.top - cam.bottom) / cam.zoom / h
                  : 2 * cam.position.distanceTo(this.target) * Math.tan(cam.fov * Math.PI / 360) / h;
         this.raycaster.params.Line.threshold = 3 * cm_per_pixel;
         const ints = orig.call(this, mouse), ray = this.raycaster.ray,
               trk = ints.filter(t => t.object.geo_object)
                         .sort((a, b) => ray.distanceToPoint(a.point) - ray.distanceToPoint(b.point));
         return trk.concat(ints.filter(t => !t.object.geo_object));
      }};
   }}
   function tracks(d) {{
      // one TPolyLine3D per track; the list option is shown as tooltip
      const lst = {{ _typename: 'TList', name: 'tracks', arr: [], opt: [] }};
      let o = 0;
      d.n.forEach((n, i) => {{
         lst.arr.push({{ _typename: 'TPolyLine3D', fN: n, fP: d.p.slice(3 * o, 3 * (o + n)),
                        fLineColor: d.c[i], fLineWidth: 1, fLineStyle: 1, fOption: '' }});
         lst.opt.push(d.l[i]);
         o += n;
      }});
      return lst;
   }}
   function run(Core) {{
      Core.settings.HandleKeys = false;
      Promise.all([{_zip(jgeo)}, {_zip(jtrk)}])
         .then(([jg, jt]) => Core.draw('{div}', Core.parse(jg), 'transp80;axis')
                                 .then(p => p.drawExtras(tracks(JSON.parse(jt))).then(() => {{ restore(p); sharpen(p); save(p); }})))
         .catch(fail);
   }}
   const servers = ['/static/', 'https://root.cern/js/7.11.0/', 'https://jsroot.gsi.de/7.11.0/'],
         path = 'build/jsroot';
   if (typeof JSROOT !== 'undefined')
      run(JSROOT);
   else if (typeof requirejs !== 'undefined') {{
      servers.forEach((s, i) => {{ servers[i] = s + path; }});
      requirejs.config({{ paths: {{ 'jsroot': servers }} }})(['jsroot'], run, fail);
   }} else {{
      const config = document.getElementById('jupyter-config-data');
      if (config)
         servers[0] = (JSON.parse(config.innerHTML || '{{}}')?.baseUrl || '/') + 'static/';
      else
         servers.shift();
      (function load() {{
         if (!servers.length) return fail('could not load JSROOT');
         import(servers.shift() + path + '.js').then(() => run(JSROOT), load);
      }})();
   }}
}})();
</script>"""


def show3d(pmin=0.0, width=700, height=700):
    """show the interactive 3D view of the last event (tracks with p >= pmin GeV)"""
    display(HTML(display3d_html(pmin, width, height)))


# --- pictures of ROOT canvases ---------------------------------------------

def _canvas_png(pad):
    """PNG picture of a ROOT canvas or pad"""
    level, ROOT.gErrorIgnoreLevel = ROOT.gErrorIgnoreLevel, ROOT.kWarning
    try:
        with tempfile.TemporaryDirectory() as d:
            name = os.path.join(d, 'canvas.png')
            pad.SaveAs(name)
            with open(name, 'rb') as f:
                return f.read()
    finally:
        ROOT.gErrorIgnoreLevel = level


def side_view_png(app):
    """PNG picture of the application's canvas (side view)"""
    return _canvas_png(app.GetDrawPad())


# --- controls -------------------------------------------------------------

def event_gui(app, pdg=-13, momentum=1.0):
    """particle and momentum controls, "Next event" button and the event view"""
    ptype = widgets.Dropdown(options=PARTICLES, value=pdg, description='Particle')
    pvalue = widgets.BoundedFloatText(value=momentum, min=0.001, max=10000, step=0.1,
                                      description='p [GeV]')
    button = widgets.Button(description='Next event', button_style='primary')
    view3d = widgets.Checkbox(value=True, description='3D view', indent=False)

    status = widgets.HTML('Choose the particle and the momentum and press <i>Next event</i>.')
    display(widgets.VBox([widgets.HBox([ptype, pvalue, button, view3d]), status]))
    # one display, replaced for every event (no piling up of views)
    event_display = display(HTML(''), display_id=True)
    view = 'gui_' + uuid.uuid4().hex   # camera kept from event to event
    log = 'event.log'                  # Geant4 output of the last event
    state = {'events': 0}

    def show_event(_=None):
        if view3d.value:
            event_display.update(HTML(display3d_html(view=view)))
        else:
            event_display.update(Image(data=side_view_png(app), format='png', width=700))

    def next_event(_=None):
        import time
        state['events'] += 1
        name = ptype.label
        what = f'event {state["events"]}: {name}, p = {pvalue.value:g} GeV'
        first = (' (the first event takes longer: Geant4 builds its physics tables)'
                 if state['events'] == 1 else '')
        button.disabled = True
        status.value = f'<b>Generating {what}</b> ...{first}'
        start = time.time()
        try:
            app.SetPrimaryPDG(ptype.value)
            app.SetPrimaryMomentum(pvalue.value)
            # Geant4 output to a file: ROOT's notebook capture would only show it
            # after the callback, and a long output could block the kernel.
            # Empty the file and append: with 'w' the reused output stream keeps
            # its old position and the new text lands behind a gap
            open(log, 'w').close()
            ROOT.gSystem.RedirectOutput(log, 'a')
            try:
                app.RunMC(1, True)
            finally:
                ROOT.gROOT.ProcessLine(_FLUSH + 'gSystem->RedirectOutput(nullptr);')
            generated = time.time() - start
            status.value = f'<b>Drawing {what}</b> ...'
            color_tracks()
            show_event()
            ntracks = ROOT.gGeoManager.GetNtracks() if ROOT.gGeoManager else 0
            status.value = (f'<b>Done: {what}</b>, {ntracks} tracks, generated in '
                            f'{generated:.1f} s, output in <code>{log}</code>'
                            f'<pre style="font-size:smaller; margin:4px 0">{_tail(log, 5)}</pre>')
        except Exception as e:
            status.value = (f'<b style="color:red">Failed: {what}</b>: '
                            f'{type(e).__name__}: {e}')
            raise
        finally:
            button.disabled = False

    button.on_click(next_event)
    view3d.observe(show_event, names='value')
    show_event()


# --- analysis macros with live display ------------------------------------

# histograms filled by the application itself, not by the macros
_INTERNAL_HISTOGRAMS = {'hEdepLong', 'hEdepTrans', 'hPrimaryEnergy'}
_hook = None   # keeps the Python event hook alive while C++ holds it


def _histograms(skip):
    """histograms in memory (gROOT) whose names are not in skip"""
    return [obj for obj in ROOT.gROOT.GetList()
            if obj.InheritsFrom('TH1') and obj.GetName() not in skip]


def _histograms_png(hists, canvas):
    """draw the histograms into a grid on canvas and return a PNG picture;
       the current pad of the macro (gPad) is left unchanged"""
    saved = ROOT.TVirtualPad.Pad()
    try:
        cols = min(len(hists), 3)
        rows = (len(hists) + cols - 1) // cols
        canvas.SetCanvasSize(320 * cols, 260 * rows)
        canvas.Clear()
        canvas.Divide(cols, rows)
        for i, h in enumerate(hists):
            canvas.cd(i + 1)
            h.Draw('colz' if h.InheritsFrom('TH2') else '')
        canvas.Update()
        return _canvas_png(canvas)
    finally:
        if saved:
            saved.cd()


# std::cout and printf are buffered: flush them, or the last lines written by a
# macro are missing from the log file until much later
_FLUSH = 'std::cout << std::flush; std::cerr << std::flush; fflush(stdout); '


def _tail(path, lines=8, flush=False):
    """last lines of a text file (HTML-escaped); flush=True writes pending
    C++/C output to the file first"""
    import html
    if flush:
        ROOT.gROOT.ProcessLine(_FLUSH)
    try:
        with open(path, errors='replace') as f:
            return html.escape(''.join(f.readlines()[-lines:]))
    except OSError:
        return ''


def run_macro(macro, interval=2.0, pmin=0.0):
    """Run an analysis macro, e.g. run_macro('dEdx.C') or run_macro('CaloAna.C+').

    While it runs, the notebook shows the event count, the last lines of the
    macro's output, the 3D view of the latest event and the histograms the macro
    fills, updated at most every `interval` seconds (3D view: tracks with
    p >= pmin GeV). The canvases the macro draws at the end are shown below.

    The complete output (std::cout, Geant4) goes to <macro>.log, e.g. dEdx.log:
    printed directly, a long output blocks the notebook kernel.
    Each macro calls app->InitMC(): run it in a fresh kernel (Geant4 can be
    initialised only once).
    """
    global _hook
    import time
    app = ROOT.TutorialApplication.Instance()
    log = os.path.splitext(macro.rstrip('+'))[0] + '.log'
    skip = _INTERNAL_HISTOGRAMS | {h.GetName() for h in _histograms(())}
    canvases_before = {c.GetName() for c in ROOT.gROOT.GetListOfCanvases()}
    status = display(HTML(f'<b>{macro}</b>: starting ...'), display_id=True)
    event_view = display(HTML(''), display_id=True)
    view = 'macro_' + uuid.uuid4().hex   # camera kept between updates
    hist_view = display(HTML(''), display_id=True)
    state = {'events': 0, 'shown': None, 'canvas': None, 'error': None}
    start = time.time()

    def update(final=False):
        now = time.time()
        word = 'done' if final else 'running'
        status.update(HTML(f'<b>{macro}</b>: {word}, {state["events"]} events, '
                           f'{now - start:.0f} s, output in <code>{log}</code>'
                           + (f' <span style="color:red">(display error: {state["error"]})</span>'
                              if state['error'] else '')
                           + f'<pre style="font-size:smaller; margin:4px 0">{_tail(log, flush=True)}</pre>'))
        if state['events'] and ROOT.gGeoManager and ROOT.gGeoManager.GetNtracks():
            event_view.update(HTML(display3d_html(pmin, view=view)))
        hists = _histograms(skip)
        if hists:
            if not state['canvas']:
                state['canvas'] = ROOT.TCanvas('run_macro_histograms', 'histograms', 960, 520)
            hist_view.update(Image(data=_histograms_png(hists, state['canvas']), format='png'))
        state['shown'] = now

    def hook():
        state['events'] += 1
        try:
            if state['shown'] is None or time.time() - state['shown'] >= interval:
                update()
        except Exception as e:      # never let a display problem stop the simulation
            state['error'] = f'{type(e).__name__}: {e}'
            state['shown'] = time.time()

    _hook = hook
    app.SetEventHook(_hook)
    # output to a file: ROOT's notebook capture reads it through a pipe that is
    # not emptied while C++ code runs, so a long output would block the kernel
    ROOT.gSystem.RedirectOutput(log, 'w')
    try:
        ROOT.gROOT.ProcessLine(f'.x {macro}')
    finally:
        ROOT.gROOT.ProcessLine(_FLUSH + 'gSystem->RedirectOutput(nullptr);')   # back to the notebook
        app.ClearEventHook()
        _hook = None
        try:
            update(final=True)
        finally:
            if state['canvas']:
                state['canvas'].Close()
            # show every canvas the macro created below the cell (ROOT's notebook
            # integration shows only canvases marked as drawn or updated)
            pad = app.GetDrawPad()
            app_canvas = ROOT.addressof(pad.GetCanvas()) if pad else None
            for c in ROOT.gROOT.GetListOfCanvases():
                if c.GetName() not in canvases_before and ROOT.addressof(c) != app_canvas:
                    c.Draw()
            _quiet(app)   # no automatic view of the app canvas (it has no tracks)

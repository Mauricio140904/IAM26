// Start the Geant4 tutorial application:
//   root -l run_g4.C              (with the ROOT GUI, needs X11 or macOS)
//   root -l --web run_g4.C        (event display in the web browser, no GUI)
//   root -l run_g4.C dEdx.C       (run an analysis macro afterwards)
// From Python/Jupyter: ROOT.gROOT.ProcessLine(".x run_g4.C(false)")
#include "TInterpreter.h"
#include "TROOT.h"
#include "TString.h"
#include "TSystem.h"

void run_g4(bool gui = true) {
  // installation prefix of Geant4 and geant4_vmc (conda environment)
  TString prefix = gSystem->Getenv("CONDA_PREFIX");
  if (prefix.IsNull()) prefix = gSystem->GetFromPipe("geant4-config --prefix");
  if (prefix.IsNull()) {
    Error("run_g4", "Geant4 not found: activate the conda environment first");
    return;
  }

  // load Geant4 VMC (pulls in Geant4, VMC and G4Root libraries)
  if (gSystem->Load("libgeant4vmc") < 0) {
    Error("run_g4", "cannot load libgeant4vmc");
    return;
  }

  // include paths for compiling the tutorial code and analysis macros (ACLiC)
  for (const char* dir : {"geant4vmc", "vmc", "g4root", "Geant4"}) {
    TString inc = prefix + "/include/" + dir;
    if (!gSystem->AccessPathName(inc)) {
      gSystem->AddIncludePath("-I" + inc);
      gInterpreter->AddIncludePath(inc);
    }
  }
  gSystem->AddIncludePath("-Iinclude");
  gInterpreter->AddIncludePath("include");
#ifdef __APPLE__
  // macOS SDK >= 27 with conda's clang: INFINITY/NAN undefined in C++23
  // unless C++ modules are switched off
  gSystem->AddIncludePath("-Xclang -fno-cxx-modules");
#endif

  // compile the tutorial application (recompiled only after changes)
  gROOT->ProcessLine(".L src/TutorialStack.cxx+g");
  gROOT->ProcessLine(".L src/TutorialApplication.cxx+g");

  // MC application
  gROOT->ProcessLine("TutorialApplication* app = new TutorialApplication()");

  // Geant4 itself is created (g4Config.C) in app->InitMC("geometry/...")

  // the ROOT GUI needs a native display (X11 or macOS);
  // otherwise use app->RunMC() and the (web) canvas
  if (gui && !gROOT->IsBatch() && !gROOT->IsWebDisplay()) {
    gROOT->ProcessLine(".L src/TutorialMainFrame.cxx+g");
    gROOT->ProcessLine("new TutorialMainFrame(app)");
  } else {
    gROOT->ProcessLine("app->Help()");
  }
}

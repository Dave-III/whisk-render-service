# Whisk Render Service

A backend rendering service for the game *Whisk* that automatically combines two player POV clips into a single synchronized speedrun video and uploads the result to YouTube.

The service supports:

* MP4 uploads
* Medal.tv clip URLs
* Automatic video composition
* YouTube uploads
* Asynchronous rendering jobs
* REST API integration

Designed for easy integration into leaderboard and speedrun submission workflows.

Client → API → Queue → Renderer → YouTube → Youtube URL

## MVP Goals

- [ ] Accept two MP4 uploads
- [ ] Accept Medal.tv clip URLs
- [ ] Render side-by-side output
- [ ] Upload final video to YouTube
- [ ] Return public/unlisted URL
- [ ] Docker deployment

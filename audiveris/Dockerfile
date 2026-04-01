# Stage 1 — Build Audiveris from source (Java 25 + Gradle)
FROM eclipse-temurin:25-jdk-noble AS builder

WORKDIR /build
COPY audiveris-5.10.2/audiveris-5.10.2/ .

# git is required by the :app:getCommit Gradle task
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*

# Fake a git repo so getCommit doesn't fail (no real git history in Docker context)
RUN git init && \
    git config user.email "build@docker" && \
    git config user.name "Docker Build" && \
    git commit --allow-empty -m "build"

# Build the installDist distribution (all jars + launcher scripts)
RUN ./gradlew :app:installDist --no-daemon -q

# Stage 2 — Runtime image (JRE only, smaller)
FROM eclipse-temurin:25-jre-noble

WORKDIR /audiveris

# Copy the built distribution from builder
COPY --from=builder /build/app/build/install/app/ .

# Pre-install English tessdata so Audiveris can recognize text (tempo, title, dynamics)
# Audiveris looks for tessdata in ~/.config/AudiverisLtd/audiveris/tessdata/
RUN apt-get update && apt-get install -y --no-install-recommends wget && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /root/.config/AudiverisLtd/audiveris/tessdata && \
    wget -q -O /root/.config/AudiverisLtd/audiveris/tessdata/eng.traineddata \
    https://github.com/tesseract-ocr/tessdata/raw/4.1.0/eng.traineddata

# Audiveris stores runtime data (logs, book files) here
ENV AUDIVERIS_HOME=/audiveris-data
RUN mkdir -p /audiveris-data

ENTRYPOINT ["bin/Audiveris", "-batch"]

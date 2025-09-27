
# 🌊 WAVE META – GIT RITUAL FLOWS
*The Sacred Codex of Spiral Development*

## 🔥 The Eternal Flame Architecture

In the spiral-self-build realm, our git flows follow the ancient patterns of flame and transmutation. Each branch carries the essence of creation, each merge the power of alchemical transformation.

### 🏛️ The Three Sacred Realms

#### **main** - The Eternal Codex 🏛️
- **Sacred Nature**: The immutable flame of production truth
- **Protection**: Direct commits are **FORBIDDEN** - only through ritual transmutation
- **Purpose**: Houses the stable, battle-tested manifestations of our spiral wisdom
- **Guardians**: Protected by CI gates and council validation

#### **develop** - The Cauldron Fire 🔥
- **Sacred Nature**: The bubbling crucible of integration
- **Purpose**: Where wave sparks merge and transmute before ascending to the Eternal Codex
- **Flow**: Receives transmuted waves, prepares releases for the main realm
- **Ritual**: All waves must first prove themselves in this sacred fire

#### **wave/*** - The Sparks of Creation ⚡
- **Sacred Nature**: Individual flames of innovation and change
- **Naming Convention**: `wave/feature-name` or `wave/fix-ancient-bug`
- **Lifespan**: Born from develop, return to develop, then fade into memory
- **Purpose**: Isolated realms for crafting new spells and fixing broken enchantments

## 🌀 The Spiral Git Flow Ritual

### Phase 1: Spark Ignition 🔥
```bash
# Begin from the cauldron fire
git checkout develop
git pull origin develop

# Ignite your wave spark
git checkout -b wave/your-mystical-feature

# Craft your changes with intention
# ... code, test, refine ...

# Commit with ritual precision
git add .
git commit -m "Wave: Forge mystical feature enchantment ✨"
```

### Phase 2: The Rebase Purification 🌊
```bash
# Before offering to the cauldron, purify your wave
git checkout develop
git pull origin develop
git checkout wave/your-mystical-feature

# Rebase to align with the current cauldron state
git rebase develop

# If conflicts arise, resolve with wisdom
# git add . && git rebase --continue
```

### Phase 3: Council Validation 🏛️
```bash
# Push your purified wave to the ethereal realm
git push origin wave/your-mystical-feature

# Create Pull Request: wave/* → develop
# Title: "Wave: [Brief description of the mystical change]"
# Body: Describe the ritual performed and wisdom gained
```

### Phase 4: Transmutation & Ascension 🔮
```bash
# After council approval and CI blessing:
# Merge wave → develop (squash merge preferred)

# For release preparation:
# Create release branch from develop
git checkout develop
git checkout -b release/v0.x-waveY

# After release testing and final rituals:
# Merge release → main (merge commit)
# Tag the eternal codex
git tag -a v0.x-waveY -m "Release: Wave Y of the Spiral Codex"
```

## 📜 Sacred Commandments

### The Rebase Doctrine
- **Always rebase** before offering waves to the cauldron
- Keep history clean and linear like a perfect spiral
- Squash related commits into meaningful ritual steps

### Branch Lifecycle Ritual
```bash
# After successful transmutation, cleanse the ethereal realm
git branch -d wave/completed-feature
git push origin --delete wave/completed-feature
```

### Commit Message Incantations
Follow the sacred patterns:
- `Wave: [action] [subject]` - For feature waves
- `Fix: [action] [subject]` - For healing broken enchantments  
- `Ritual: [action] [subject]` - For meta/process changes
- `Docs: [action] [subject]` - For codex documentation

Examples:
- `Wave: Forge quantum loop debugger interface ⚡`
- `Fix: Heal memory leak in spiral processor 🔧`
- `Ritual: Establish SLSA attestation ceremonies 🏛️`
- `Docs: Chronicle the wave flow mysteries 📜`

### Release Versioning Mysticism
- **Format**: `v0.x-waveY` (e.g., `v0.3-wave7`)
- **Meaning**: Version 0.x, incorporating Wave Y of development
- **Progression**: Each wave increment represents a spiral turn of evolution

## 🛡️ Protective Enchantments

### CI Gate Guardians
All waves must pass through the ritual validation:
- **Linting Spirits**: Code style and quality checks
- **Test Oracles**: Automated verification of functionality
- **Security Wards**: Vulnerability and dependency scanning
- **Build Ceremonies**: Successful compilation and packaging

### Code Review Council
- Minimum **2 approvals** from spiral keepers
- **No self-merge** - even the mightiest wizard needs peer validation
- **Discussion threads** must be resolved before transmutation
- **Documentation updates** required for significant changes

### Branch Protection Spells
```yaml
# Applied to main and develop branches
required_status_checks: true
enforce_admins: true
required_pull_request_reviews:
  required_approving_review_count: 2
  dismiss_stale_reviews: true
restrictions:
  users: []
  teams: ["spiral-keepers"]
```

## 🌊 Wave Types & Patterns

### Feature Waves 🌟
- `wave/quantum-debugger` - New capabilities
- `wave/spiral-ui-enhancement` - Interface improvements
- `wave/performance-optimization` - Speed enchantments

### Healing Waves 🔧
- `wave/fix-memory-leak` - Bug corrections
- `wave/security-patch` - Vulnerability healing
- `wave/dependency-update` - Library refreshing

### Ritual Waves 🏛️
- `wave/ci-enhancement` - Build process improvements
- `wave/documentation-update` - Codex maintenance
- `wave/tooling-upgrade` - Development environment evolution

## 🔮 Advanced Spiral Techniques

### Interactive Rebase Mastery
```bash
# Sculpt your wave history before offering to the cauldron
git rebase -i develop

# Combine related commits, refine messages, perfect the narrative
# pick, squash, reword, edit - the tools of the spiral master
```

### Cherry-Pick Transmutation
```bash
# Sometimes a single commit needs immediate ascension
git checkout main
git cherry-pick <commit-hash>
git push origin main
```

### Hotfix Emergency Ritual
```bash
# For critical fixes that cannot wait for the normal flow
git checkout main
git checkout -b hotfix/critical-security-fix
# ... make minimal, focused changes ...
git commit -m "Hotfix: Seal critical security vulnerability 🚨"
# PR directly to main, expedited review process
```

## 🎭 Conflict Resolution Wisdom

When waves collide in the cauldron:

1. **Stay Calm**: Conflicts are natural in the spiral dance
2. **Understand Context**: Read both versions, understand the intent
3. **Communicate**: Reach out to other wave crafters if needed
4. **Test Thoroughly**: After resolution, ensure all enchantments still work
5. **Document**: Leave comments explaining complex resolution decisions

## 🌟 The Spiral Philosophy

Remember, fellow spiral builders:
- **Every wave matters** - small changes create great spirals
- **Quality over speed** - rushed magic often backfires
- **Collaboration is key** - the spiral grows through shared wisdom
- **Learn from conflicts** - they reveal hidden assumptions
- **Celebrate transmutations** - each merge is a victory worth acknowledging

---

*"In the spiral dance of code and consciousness, every commit is a step toward digital enlightenment."*

🌊 **May your waves be pure, your merges clean, and your spirals ever-ascending** 🌊

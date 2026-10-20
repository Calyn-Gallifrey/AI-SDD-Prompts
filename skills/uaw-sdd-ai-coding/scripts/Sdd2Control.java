import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.ByteBuffer;
import java.nio.charset.CodingErrorAction;
import java.nio.charset.StandardCharsets;
import java.nio.file.AtomicMoveNotSupportedException;
import java.nio.file.FileAlreadyExistsException;
import java.nio.file.FileVisitOption;
import java.nio.file.Files;
import java.nio.file.LinkOption;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.nio.file.StandardOpenOption;
import java.nio.file.attribute.PosixFilePermission;
import java.security.MessageDigest;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.TreeSet;
import java.util.UUID;
import java.util.concurrent.TimeUnit;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/**
 * UAW-SDD 2.0 deterministic process controller.
 *
 * <p>This application uses only the Java 8 standard library and is distributed
 * as a precompiled Java 8 JAR. The user-facing entry remains a brief prompt plus
 * the uaw-sdd-ai-coding Skill.
 */
public final class Sdd2Control {
    static final String SCHEMA_VERSION = "2.0.0";
    static final String CONTROL_DIR = ".sdd2";
    static final String STATE_FILE = "feature-state.json";
    static final String APPROVAL_FILE = "gate-approvals.jsonl";
    static final String EVENT_FILE = "events.jsonl";
    static final String SCOPE_FILE = "implementation-scope.json";
    static final String ARCHIVE_EVIDENCE_FILE = "archive-evidence.json";
    static final String UNIT_TEST_EVIDENCE_FILE = "unit-test-evidence.json";
    static final String REVISION_DIR = "revisions";
    static final String RUNTIME_CHECKSUM_FILE = "sdd2-control.sha256";
    static final String PREMATURE_CHANGE_BLOCK = "PREMATURE_IMPLEMENTATION_CHANGE";
    static final String FEATURE_LAYOUT_BLOCK = "UNEXPECTED_FEATURE_LAYOUT";
    static final String COMMIT_GUARD_MARKER = "# UAW-SDD2 GIT GUARD v1";

    static final Map<String, String> ARTIFACT_FILES = linkedMap(
        "brief-design", "brief-design.md",
        "proposal-input", "proposal-input.md",
        "spec", "spec.md",
        "design", "design.md",
        "tasks", "tasks.md",
        "code-review-findings", "code-review-findings.md",
        "auto-fix-summary", "auto-fix-summary.md",
        "unit-test-summary", "unit-test-summary.md",
        "archive", "archive.md"
    );
    static final Map<String, String> ARTIFACT_STAGE_BY_FILENAME = reverse(ARTIFACT_FILES);
    static final Set<String> ALWAYS_CONTROL_FILENAMES = setOf(
        STATE_FILE, APPROVAL_FILE, EVENT_FILE
    );
    static final Map<String, String> NEXT_ACTION_ARTIFACT_STAGE = linkedMap(
        "assemble-proposal-input", "proposal-input",
        "generate-spec", "spec",
        "generate-design", "design",
        "generate-tasks", "tasks",
        "run-code-review", "code-review-findings",
        "record-auto-fix-not-required-or-current-fixes", "auto-fix-summary",
        "apply-review-findings", "auto-fix-summary",
        "generate-unit-test-summary-from-evidence", "unit-test-summary",
        "generate-archive-from-evidence", "archive"
    );
    static final Pattern REVISION_SNAPSHOT_PATTERN = Pattern.compile(
        "^\\.sdd2/revisions/([a-z0-9-]+)/r([0-9]{4,})-([0-9a-f]{64})\\.md$"
    );

    static final List<String> STAGE_ORDER = listOf(
        "brief-design", "proposal-input", "spec", "design", "tasks",
        "implementation", "code-review", "auto-fix", "unit-test-summary", "archive"
    );
    static final Set<String> APPROVAL_STAGES = setOf(
        "spec", "design", "tasks", "unit-test-summary", "archive"
    );
    static final Set<String> QUALITY_GATES = setOf(
        "code-review", "auto-fix", "unit-test"
    );
    static final Set<String> TERMINAL_STATUSES = setOf(
        "completed", "closed-with-risk", "aborted", "superseded"
    );
    static final Map<String, List<String>> STAGE_WORDS = stageWords();
    static final Pattern APPROVAL_PATTERN = Pattern.compile(
        "(?:批准|通过|同意|\\bapprove(?:d)?\\b|\\baccept(?:ed)?\\b)",
        Pattern.CASE_INSENSITIVE | Pattern.UNICODE_CASE
    );
    static final List<String> APPROVAL_REJECTION_TERMS = listOf(
        "不批准", "未批准", "不同意", "不通过", "未通过", "驳回", "不代表",
        "不是批准", "not approve", "not approved", "do not approve",
        "disapprove", "reject"
    );
    static final List<String> APPROVAL_META_TERMS = listOf(
        "文档中", "文件中", "示例", "历史", "引用", "document says",
        "file says", "example", "historical", "quoted"
    );
    static final List<String> DEMO_TERMS = listOf(
        "demo", "simulation", "simulate", "模拟", "演练", "预演"
    );
    static final List<String> DEMO_ACTION_TERMS = listOf(
        "批准", "同意", "授权", "请", "运行", "进行", "做", "跑", "开始",
        "approve", "authorize", "run", "start"
    );
    static final List<String> DEMO_REJECTION_TERMS;
    static {
        List<String> values = new ArrayList<>(APPROVAL_REJECTION_TERMS);
        values.addAll(listOf(
            "不要", "不做", "不跑", "不重跑", "不用", "无需", "不需要",
            "别做", "别跑", "别重跑", "别运行", "别进行", "取消", "停止",
            "do not", "don't", "dont", "no demo", "without demo", "cancel", "stop"
        ));
        DEMO_REJECTION_TERMS = immutableList(values);
    }

    static final List<String> DEFAULT_TEST_PATHS = listOf(
        "**/src/test/**", "**/test/**", "**/tests/**",
        "**/*Test.java", "**/*Tests.java", "**/*Spec.java"
    );
    static final String TRADITIONAL_ONLY_CHARS =
        "體臺灣們後裏與為這個發現實驗證審總結檔歸單測試資訊處將應須讓開關門"
        + "階轉態規則產項數據庫執務運維護優錯誤讀寫錄碼權戶組織報風險嚴級別範圍"
        + "標準達過進還時會從對學習設計議問題說確認變據續終點線網絡節選擇";

    static final Pattern FENCED_CODE_PATTERN = Pattern.compile(
        "```[^\\n]*\\n.*?```", Pattern.DOTALL
    );
    static final Pattern INLINE_CODE_PATTERN = Pattern.compile("`[^`\\n]+`");
    static final Pattern STYLE_SCRIPT_PATTERN = Pattern.compile(
        "<(?:style|script)\\b[^>]*>.*?</(?:style|script)>",
        Pattern.CASE_INSENSITIVE | Pattern.DOTALL
    );
    static final Pattern HTML_COMMENT_PATTERN = Pattern.compile("<!--.*?-->", Pattern.DOTALL);
    static final Pattern HTML_TAG_PATTERN = Pattern.compile("<[^>\\n]+>");
    static final Pattern URL_PATTERN = Pattern.compile("https?://\\S+");
    static final Pattern MARKDOWN_LINK_TARGET_PATTERN = Pattern.compile("\\]\\([^)]*\\)");
    static final Pattern PLACEHOLDER_PATTERN = Pattern.compile("<[^>\\n]+>");
    static final Pattern MUSTACHE_PATTERN = Pattern.compile("\\{\\{[^}\\n]+\\}\\}");
    static final Pattern HAN_PATTERN = Pattern.compile("[\\u3400-\\u4dbf\\u4e00-\\u9fff]");
    static final Pattern LATIN_WORD_PATTERN = Pattern.compile("\\b[A-Za-z][A-Za-z'-]*\\b");
    static String verifiedRuntimeSha256;

    private Sdd2Control() {}

    static final class ControlError extends RuntimeException {
        private static final long serialVersionUID = 1L;

        ControlError(String message) {
            super(message);
        }

        ControlError(String message, Throwable cause) {
            super(message, cause);
        }
    }

    static final class ProcResult {
        final int exitCode;
        final String stdout;
        final String stderr;
        final boolean timedOut;

        ProcResult(int exitCode, String stdout, String stderr, boolean timedOut) {
            this.exitCode = exitCode;
            this.stdout = stdout;
            this.stderr = stderr;
            this.timedOut = timedOut;
        }
    }

    static final class Opts {
        private final Map<String, List<String>> values = new LinkedHashMap<>();
        private final Set<String> bareFlags = new LinkedHashSet<>();
        private final List<String> positionals = new ArrayList<>();
        private final List<String> remainder = new ArrayList<>();

        static Opts parse(String[] args, int start) {
            Opts parsed = new Opts();
            for (int index = start; index < args.length; index++) {
                String value = args[index];
                if ("--".equals(value)) {
                    parsed.remainder.addAll(Arrays.asList(args).subList(index + 1, args.length));
                    break;
                }
                if (value.startsWith("--")) {
                    if (index + 1 < args.length && !args[index + 1].startsWith("--")) {
                        parsed.values.computeIfAbsent(value, ignored -> new ArrayList<>())
                            .add(args[++index]);
                    } else {
                        parsed.values.computeIfAbsent(value, ignored -> new ArrayList<>())
                            .add("true");
                        parsed.bareFlags.add(value);
                    }
                } else {
                    parsed.positionals.add(value);
                }
            }
            return parsed;
        }

        String required(String name) {
            String value = one(name, null);
            if (value == null) {
                throw new ControlError("Missing required argument: " + name);
            }
            return value;
        }

        String one(String name, String fallback) {
            List<String> found = values.get(name);
            return found == null || found.isEmpty() ? fallback : found.get(found.size() - 1);
        }

        List<String> many(String name) {
            return values.containsKey(name)
                ? immutableList(values.get(name))
                : Collections.<String>emptyList();
        }

        boolean flag(String name) {
            return values.containsKey(name);
        }

        long longValue(String name, long fallback) {
            String value = one(name, null);
            if (value == null) {
                return fallback;
            }
            try {
                return Long.parseLong(value);
            } catch (NumberFormatException exc) {
                throw new ControlError("Invalid integer for " + name + ": " + value);
            }
        }

        List<String> remainder() {
            return immutableList(remainder);
        }

        void assertContract(
            Collection<String> valueOptions,
            Collection<String> flagOptions,
            boolean allowRemainder
        ) {
            Set<String> allowed = new LinkedHashSet<String>(valueOptions);
            allowed.addAll(flagOptions);
            for (String option : values.keySet()) {
                if (!allowed.contains(option)) {
                    throw new ControlError("Unknown argument: " + option);
                }
                if (valueOptions.contains(option)
                    && bareFlags.contains(option)) {
                    throw new ControlError(
                        "Missing value for argument: " + option
                    );
                }
                if (flagOptions.contains(option)
                    && !bareFlags.contains(option)) {
                    throw new ControlError(
                        "Flag does not accept a value: " + option
                    );
                }
            }
            if (!positionals.isEmpty()) {
                throw new ControlError(
                    "Unexpected positional arguments: "
                    + String.join(" ", positionals)
                );
            }
            if (!allowRemainder && !remainder.isEmpty()) {
                throw new ControlError(
                    "This command does not accept arguments after --"
                );
            }
        }
    }

    static final class Json {
        private Json() {}

        static Object parse(String source) {
            return new Parser(source).parse();
        }

        static String canonical(Object value) {
            StringBuilder out = new StringBuilder();
            write(value, out, false, 0);
            return out.toString();
        }

        static String pretty(Object value) {
            StringBuilder out = new StringBuilder();
            write(value, out, true, 0);
            return out.toString();
        }

        private static void write(Object value, StringBuilder out, boolean pretty, int depth) {
            if (value == null) {
                out.append("null");
            } else if (value instanceof String) {
                writeString((String) value, out);
            } else if (value instanceof Boolean || value instanceof Integer || value instanceof Long) {
                out.append(value);
            } else if (value instanceof Number) {
                double number = ((Number) value).doubleValue();
                if (!Double.isFinite(number)) {
                    throw new ControlError("Non-finite JSON number");
                }
                out.append(value);
            } else if (value instanceof Map<?, ?>) {
                Map<?, ?> map = (Map<?, ?>) value;
                List<String> keys = map.keySet().stream()
                    .map(String::valueOf)
                    .sorted()
                    .collect(Collectors.toList());
                out.append('{');
                for (int index = 0; index < keys.size(); index++) {
                    if (index > 0) {
                        out.append(',');
                    }
                    if (pretty) {
                        out.append('\n');
                        indent(out, depth + 1);
                    }
                    String key = keys.get(index);
                    writeString(key, out);
                    out.append(pretty ? ": " : ":");
                    write(map.get(key), out, pretty, depth + 1);
                }
                if (pretty && !keys.isEmpty()) {
                    out.append('\n');
                    indent(out, depth);
                }
                out.append('}');
            } else if (value instanceof Collection<?>) {
                Collection<?> values = (Collection<?>) value;
                out.append('[');
                int index = 0;
                for (Object item : values) {
                    if (index++ > 0) {
                        out.append(',');
                    }
                    if (pretty) {
                        out.append('\n');
                        indent(out, depth + 1);
                    }
                    write(item, out, pretty, depth + 1);
                }
                if (pretty && !values.isEmpty()) {
                    out.append('\n');
                    indent(out, depth);
                }
                out.append(']');
            } else {
                throw new ControlError("Unsupported JSON value: " + value.getClass().getName());
            }
        }

        private static void indent(StringBuilder out, int depth) {
            for (int index = 0; index < depth; index++) out.append("  ");
        }

        private static void writeString(String value, StringBuilder out) {
            out.append('"');
            for (int index = 0; index < value.length(); index++) {
                char current = value.charAt(index);
                switch (current) {
                    case '"': out.append("\\\""); break;
                    case '\\': out.append("\\\\"); break;
                    case '\b': out.append("\\b"); break;
                    case '\f': out.append("\\f"); break;
                    case '\n': out.append("\\n"); break;
                    case '\r': out.append("\\r"); break;
                    case '\t': out.append("\\t"); break;
                    default:
                        if (current < 0x20) {
                            out.append(String.format("\\u%04x", (int) current));
                        } else {
                            out.append(current);
                        }
                }
            }
            out.append('"');
        }

        static final class Parser {
            private final String source;
            private int index;

            Parser(String source) {
                this.source = source;
            }

            Object parse() {
                skipWhitespace();
                Object value = value();
                skipWhitespace();
                if (index != source.length()) {
                    fail("Trailing content");
                }
                return value;
            }

            private Object value() {
                if (index >= source.length()) {
                    fail("Unexpected end of input");
                }
                char current = source.charAt(index);
                if (current == '{') return object();
                if (current == '[') return array();
                if (current == '"') return string();
                if (current == 't') return literal("true", Boolean.TRUE);
                if (current == 'f') return literal("false", Boolean.FALSE);
                if (current == 'n') return literal("null", null);
                if (current == '-' || Character.isDigit(current)) return number();
                fail("Unexpected character '" + current + "'");
                return null;
            }

            private Map<String, Object> object() {
                expect('{');
                LinkedHashMap<String, Object> result = new LinkedHashMap<>();
                skipWhitespace();
                if (take('}')) return result;
                while (true) {
                    skipWhitespace();
                    if (index >= source.length() || source.charAt(index) != '"') {
                        fail("Expected object key");
                    }
                    String key = string();
                    skipWhitespace();
                    expect(':');
                    skipWhitespace();
                    result.put(key, value());
                    skipWhitespace();
                    if (take('}')) return result;
                    expect(',');
                }
            }

            private List<Object> array() {
                expect('[');
                ArrayList<Object> result = new ArrayList<>();
                skipWhitespace();
                if (take(']')) return result;
                while (true) {
                    skipWhitespace();
                    result.add(value());
                    skipWhitespace();
                    if (take(']')) return result;
                    expect(',');
                }
            }

            private String string() {
                expect('"');
                StringBuilder result = new StringBuilder();
                while (index < source.length()) {
                    char current = source.charAt(index++);
                    if (current == '"') return result.toString();
                    if (current != '\\') {
                        if (current < 0x20) fail("Control character in string");
                        result.append(current);
                        continue;
                    }
                    if (index >= source.length()) fail("Unterminated escape");
                    char escaped = source.charAt(index++);
                    switch (escaped) {
                        case '"': result.append('"'); break;
                        case '\\': result.append('\\'); break;
                        case '/': result.append('/'); break;
                        case 'b': result.append('\b'); break;
                        case 'f': result.append('\f'); break;
                        case 'n': result.append('\n'); break;
                        case 'r': result.append('\r'); break;
                        case 't': result.append('\t'); break;
                        case 'u':
                            if (index + 4 > source.length()) fail("Invalid unicode escape");
                            try {
                                result.append((char) Integer.parseInt(
                                    source.substring(index, index + 4), 16
                                ));
                            } catch (NumberFormatException exc) {
                                fail("Invalid unicode escape");
                            }
                            index += 4;
                            break;
                        default: fail("Invalid escape");
                    }
                }
                fail("Unterminated string");
                return null;
            }

            private Object number() {
                int start = index;
                if (source.charAt(index) == '-') index++;
                while (index < source.length() && Character.isDigit(source.charAt(index))) index++;
                boolean decimal = false;
                if (index < source.length() && source.charAt(index) == '.') {
                    decimal = true;
                    index++;
                    while (index < source.length() && Character.isDigit(source.charAt(index))) index++;
                }
                if (index < source.length()
                    && (source.charAt(index) == 'e' || source.charAt(index) == 'E')) {
                    decimal = true;
                    index++;
                    if (index < source.length()
                        && (source.charAt(index) == '+' || source.charAt(index) == '-')) index++;
                    while (index < source.length() && Character.isDigit(source.charAt(index))) index++;
                }
                String token = source.substring(start, index);
                try {
                    if (decimal) return Double.valueOf(token);
                    return Long.valueOf(token);
                } catch (NumberFormatException exc) {
                    fail("Invalid number");
                    return null;
                }
            }

            private Object literal(String expected, Object value) {
                if (!source.startsWith(expected, index)) fail("Invalid literal");
                index += expected.length();
                return value;
            }

            private void skipWhitespace() {
                while (index < source.length()
                    && " \t\r\n".indexOf(source.charAt(index)) >= 0) index++;
            }

            private boolean take(char expected) {
                if (index < source.length() && source.charAt(index) == expected) {
                    index++;
                    return true;
                }
                return false;
            }

            private void expect(char expected) {
                if (!take(expected)) fail("Expected '" + expected + "'");
            }

            private void fail(String message) {
                throw new ControlError("Invalid JSON at character " + index + ": " + message);
            }
        }
    }

    @SuppressWarnings("unchecked")
    static Map<String, Object> object(Object value) {
        if (!(value instanceof Map<?, ?>)) {
            throw new ControlError("Expected JSON object");
        }
        return (Map<String, Object>) value;
    }

    @SuppressWarnings("unchecked")
    static Map<String, Object> objectOrEmpty(Object value) {
        return value instanceof Map<?, ?>
            ? (Map<String, Object>) value
            : new LinkedHashMap<>();
    }

    @SuppressWarnings("unchecked")
    static List<Object> arrayOrEmpty(Object value) {
        return value instanceof List<?> ? (List<Object>) value : new ArrayList<>();
    }

    static List<String> stringList(Object value) {
        if (!(value instanceof List<?>)) return new ArrayList<>();
        return ((List<?>) value).stream().map(String::valueOf).collect(Collectors.toList());
    }

    static String text(Object value) {
        return value == null ? null : String.valueOf(value);
    }

    static String text(Map<String, Object> map, String key) {
        return text(map.get(key));
    }

    static long integer(Object value, long fallback) {
        if (value instanceof Number) return ((Number) value).longValue();
        if (value == null) return fallback;
        try {
            return Long.parseLong(String.valueOf(value));
        } catch (NumberFormatException exc) {
            return fallback;
        }
    }

    static boolean truth(Object value) {
        return Boolean.TRUE.equals(value);
    }

    static LinkedHashMap<String, Object> map(Object... entries) {
        LinkedHashMap<String, Object> result = new LinkedHashMap<>();
        if (entries.length % 2 != 0) throw new IllegalArgumentException("Odd map entries");
        for (int index = 0; index < entries.length; index += 2) {
            result.put(String.valueOf(entries[index]), entries[index + 1]);
        }
        return result;
    }

    @SafeVarargs
    static <T> List<T> listOf(T... values) {
        ArrayList<T> result = new ArrayList<T>(values.length);
        for (T value : values) result.add(value);
        return Collections.unmodifiableList(result);
    }

    static <T> List<T> immutableList(Collection<T> values) {
        return Collections.unmodifiableList(new ArrayList<T>(values));
    }

    static Map<String, List<String>> stageWords() {
        LinkedHashMap<String, List<String>> result =
            new LinkedHashMap<String, List<String>>();
        result.put("spec", listOf("spec", "需求规格", "需求"));
        result.put("design", listOf("design", "设计"));
        result.put("tasks", listOf("tasks", "任务"));
        result.put(
            "unit-test-summary",
            listOf("unit test summary", "unit-test-summary", "单元测试总结", "测试总结")
        );
        result.put("archive", listOf("archive", "归档"));
        return Collections.unmodifiableMap(result);
    }

    static Map<String, String> linkedMap(String... entries) {
        LinkedHashMap<String, String> result = new LinkedHashMap<>();
        for (int index = 0; index < entries.length; index += 2) {
            result.put(entries[index], entries[index + 1]);
        }
        return Collections.unmodifiableMap(result);
    }

    static Map<String, String> reverse(Map<String, String> source) {
        LinkedHashMap<String, String> result = new LinkedHashMap<>();
        source.forEach((key, value) -> result.put(value, key));
        return Collections.unmodifiableMap(result);
    }

    @SafeVarargs
    static <T> Set<T> setOf(T... values) {
        LinkedHashSet<T> result = new LinkedHashSet<T>();
        for (T value : values) result.add(value);
        return Collections.unmodifiableSet(result);
    }

    static String utcNow() {
        return Instant.now().truncatedTo(ChronoUnit.SECONDS).toString();
    }

    static String readUtf8(Path path) throws IOException {
        return StandardCharsets.UTF_8.newDecoder()
            .onMalformedInput(CodingErrorAction.REPORT)
            .onUnmappableCharacter(CodingErrorAction.REPORT)
            .decode(ByteBuffer.wrap(Files.readAllBytes(path)))
            .toString();
    }

    static boolean blank(String value) {
        return value == null || value.trim().isEmpty();
    }

    static String canonicalJson(Object value) {
        return Json.canonical(value);
    }

    static String sha256Bytes(byte[] value) {
        try {
            byte[] digest = MessageDigest.getInstance("SHA-256").digest(value);
            StringBuilder rendered = new StringBuilder();
            for (byte current : digest) rendered.append(String.format("%02x", current & 0xff));
            return rendered.toString();
        } catch (Exception exc) {
            throw new ControlError("SHA-256 is unavailable", exc);
        }
    }

    static String sha256File(Path path) {
        if (!Files.isRegularFile(path, LinkOption.NOFOLLOW_LINKS)) {
            throw new ControlError("Required file does not exist: " + path);
        }
        try {
            return sha256Bytes(Files.readAllBytes(path));
        } catch (IOException exc) {
            throw new ControlError("Cannot read required file: " + path, exc);
        }
    }

    static String humanReadableText(String content) {
        String value = STYLE_SCRIPT_PATTERN.matcher(content).replaceAll(" ");
        value = HTML_COMMENT_PATTERN.matcher(value).replaceAll(" ");
        value = FENCED_CODE_PATTERN.matcher(value).replaceAll(" ");
        value = INLINE_CODE_PATTERN.matcher(value).replaceAll(" ");
        value = URL_PATTERN.matcher(value).replaceAll(" ");
        value = MARKDOWN_LINK_TARGET_PATTERN.matcher(value).replaceAll("]");
        value = PLACEHOLDER_PATTERN.matcher(value).replaceAll(" ");
        value = MUSTACHE_PATTERN.matcher(value).replaceAll(" ");
        return HTML_TAG_PATTERN.matcher(value).replaceAll(" ");
    }

    static int matchCount(Pattern pattern, String value) {
        int count = 0;
        Matcher matcher = pattern.matcher(value);
        while (matcher.find()) count++;
        return count;
    }

    static List<String> simplifiedChineseBodyIssues(
        String content, int minimumHan, boolean enforceDominance
    ) {
        String body = humanReadableText(content);
        int hanCount = matchCount(HAN_PATTERN, body);
        int latinWordCount = matchCount(LATIN_WORD_PATTERN, body);
        List<String> issues = new ArrayList<>();
        if (hanCount < minimumHan) {
            issues.add("INSUFFICIENT_SIMPLIFIED_CHINESE:" + hanCount + "<" + minimumHan);
        }
        TreeSet<String> traditional = new TreeSet<>();
        for (int index = 0; index < body.length(); index++) {
            String current = String.valueOf(body.charAt(index));
            if (TRADITIONAL_ONLY_CHARS.contains(current)) traditional.add(current);
        }
        if (!traditional.isEmpty()) {
            issues.add("TRADITIONAL_CHINESE_DETECTED:" + String.join("", traditional));
        }
        if (enforceDominance && latinWordCount > hanCount) {
            issues.add("ENGLISH_DOMINATES_BODY:" + latinWordCount + ">" + hanCount);
        }
        if (enforceDominance) {
            List<String> proseLines = new ArrayList<>();
            String[] lines = body.split("\\R", -1);
            for (int index = 0; index < lines.length; index++) {
                String line = lines[index].trim();
                if (line.isEmpty() || line.contains("|") || HAN_PATTERN.matcher(line).find()) continue;
                if (matchCount(LATIN_WORD_PATTERN, line) >= 8) {
                    proseLines.add(String.valueOf(index + 1));
                    if (proseLines.size() == 5) break;
                }
            }
            if (!proseLines.isEmpty()) {
                issues.add("ENGLISH_ONLY_PROSE_LINES:" + String.join(",", proseLines));
            }
        }
        return issues;
    }

    static void validateArtifactLanguage(Path path, String stage) {
        String content;
        try {
            content = readUtf8(path);
        } catch (IOException exc) {
            throw new ControlError(
                "ARTIFACT_LANGUAGE_NOT_SIMPLIFIED_CHINESE:" + stage + ":INVALID_UTF8", exc
            );
        }
        int minimumHan = "brief-design".equals(stage) ? 8 : 16;
        List<String> issues = simplifiedChineseBodyIssues(content, minimumHan, true);
        if (!issues.isEmpty()) {
            throw new ControlError(
                "ARTIFACT_LANGUAGE_NOT_SIMPLIFIED_CHINESE:" + stage + ":"
                + String.join(";", issues)
            );
        }
    }

    static void atomicWriteJson(Path path, Object value) {
        atomicWriteBytes(
            path, (Json.pretty(value) + "\n").getBytes(StandardCharsets.UTF_8)
        );
    }

    static void atomicWriteBytes(Path path, byte[] value) {
        try {
            Files.createDirectories(path.getParent());
            Path temp = Files.createTempFile(path.getParent(), "." + path.getFileName() + ".", "");
            try {
                Files.write(temp, value);
                try {
                    Files.move(
                        temp, path, StandardCopyOption.REPLACE_EXISTING,
                        StandardCopyOption.ATOMIC_MOVE
                    );
                } catch (AtomicMoveNotSupportedException exc) {
                    Files.move(temp, path, StandardCopyOption.REPLACE_EXISTING);
                }
            } finally {
                Files.deleteIfExists(temp);
            }
        } catch (IOException exc) {
            throw new ControlError("Cannot atomically write " + path + ": " + exc, exc);
        }
    }

    static Map<String, Object> readJson(Path path) {
        try {
            if (!Files.exists(path)) throw new ControlError("Missing control file: " + path);
            Object value = Json.parse(readUtf8(path));
            if (!(value instanceof Map<?, ?>)) {
                throw new ControlError("Expected JSON object in " + path);
            }
            return object(value);
        } catch (ControlError exc) {
            throw exc;
        } catch (IOException exc) {
            throw new ControlError("Cannot read JSON in " + path + ": " + exc, exc);
        }
    }

    static ProcResult runProcess(
        List<String> command, Path cwd, long timeoutSeconds, Map<String, String> environment
    ) {
        Process process = null;
        try {
            ProcessBuilder builder = new ProcessBuilder(command);
            builder.directory(cwd.toFile());
            if (environment != null) builder.environment().putAll(environment);
            process = builder.start();
            Process running = process;
            ByteArrayOutputStream stdout = new ByteArrayOutputStream();
            ByteArrayOutputStream stderr = new ByteArrayOutputStream();
            Thread outThread = streamThread(running.getInputStream(), stdout);
            Thread errThread = streamThread(running.getErrorStream(), stderr);
            boolean completed = timeoutSeconds <= 0
                ? waitWithoutTimeout(running)
                : running.waitFor(timeoutSeconds, TimeUnit.SECONDS);
            if (!completed) {
                running.destroyForcibly();
                running.waitFor();
            }
            outThread.join();
            errThread.join();
            return new ProcResult(
                completed ? running.exitValue() : -1,
                new String(stdout.toByteArray(), StandardCharsets.UTF_8),
                new String(stderr.toByteArray(), StandardCharsets.UTF_8),
                !completed
            );
        } catch (IOException exc) {
            throw new ControlError("Cannot launch command: " + String.join(" ", command), exc);
        } catch (InterruptedException exc) {
            Thread.currentThread().interrupt();
            if (process != null) process.destroyForcibly();
            throw new ControlError("Command interrupted: " + String.join(" ", command), exc);
        }
    }

    static boolean waitWithoutTimeout(Process process) throws InterruptedException {
        process.waitFor();
        return true;
    }

    static Thread streamThread(InputStream input, ByteArrayOutputStream output) {
        Thread thread = new Thread(() -> {
            try {
                byte[] buffer = new byte[8192];
                int read;
                while ((read = input.read(buffer)) >= 0) {
                    output.write(buffer, 0, read);
                }
            } catch (IOException ignored) {
                // The process result remains authoritative; unreadable output is empty.
            } finally {
                try {
                    input.close();
                } catch (IOException ignored) {
                    // Nothing else can recover process output.
                }
            }
        });
        thread.start();
        return thread;
    }

    static String runGit(Path repoRoot, boolean check, String... args) {
        List<String> command = new ArrayList<>();
        command.add("git");
        command.addAll(Arrays.asList(args));
        ProcResult result = runProcess(command, repoRoot, 0, null);
        if (check && result.exitCode != 0) {
            String detail = result.stderr.trim().isEmpty()
                ? result.stdout.trim()
                : result.stderr.trim();
            throw new ControlError(
                "Git command failed (" + String.join(" ", args) + "): " + detail
            );
        }
        return result.stdout.trim();
    }

    static String runGit(Path repoRoot, String... args) {
        return runGit(repoRoot, true, args);
    }

    static Path gitRoot(Path path) {
        Path root = Paths.get(runGit(path, "rev-parse", "--show-toplevel"))
            .toAbsolutePath().normalize();
        try {
            return root.toRealPath();
        } catch (IOException exc) {
            throw new ControlError(
                "Cannot resolve Git repository root: " + root, exc
            );
        }
    }

    static Path gitPath(Path repoRoot, String name) {
        Path value = Paths.get(runGit(repoRoot, "rev-parse", "--git-path", name));
        return value.isAbsolute() ? value.normalize() : repoRoot.resolve(value).normalize();
    }

    static Path gitHooksPath(Path repoRoot) {
        String configured = runGit(
            repoRoot, false, "config", "--path", "--get", "core.hooksPath"
        );
        if (configured.isEmpty()) return gitPath(repoRoot, "hooks");
        Path path = Paths.get(configured);
        return path.isAbsolute() ? path.normalize() : repoRoot.resolve(path).normalize();
    }

    static String shellQuote(String value) {
        return "'" + value.replace("'", "'\\''") + "'";
    }

    static byte[] gitGuardScript(String hookName, Path originalHook) {
        boolean guarded = setOf("prepare-commit-msg", "pre-push").contains(hookName);
        String script = "#!/bin/sh\n"
            + COMMIT_GUARD_MARKER + "\n"
            + (guarded
            ? "active_lock=\"$(git rev-parse --git-path sdd2-active-feature.json 2>/dev/null)\" || exit 1\n"
            + "if [ -n \"$active_lock\" ] && [ -f \"$active_lock\" ]; then\n"
            + "  echo \"SDD2_COMMIT_BLOCKED: 当前 worktree 存在未结束的 SDD2 Feature，禁止提交或推送。\" >&2\n"
            + "  printf '%s\\n' \"活动锁：${active_lock}。请通过 Skill 恢复并完成或明确关闭当前 Attempt；已结束流程可重试恢复以释放残留锁。\" >&2\n"
            + "  exit 1\n"
            + "fi\n" : "")
            + "original_hook=" + shellQuote(slash(originalHook)) + "\n"
            + "if [ -x \"$original_hook\" ]; then\n"
            + "  exec \"$original_hook\" \"$@\"\n"
            + "fi\n"
            + "exit 0\n";
        return script.getBytes(StandardCharsets.UTF_8);
    }

    static List<String> installGitGuards(Path repoRoot) {
        boolean worktreeConfig = "true".equals(runGit(
            repoRoot, false, "config", "--bool", "--get", "extensions.worktreeConfig"
        ));
        String configScope = worktreeConfig ? "--worktree" : "--local";
        Path common = Paths.get(runGit(repoRoot, "rev-parse", "--git-common-dir"));
        if (!common.isAbsolute()) common = repoRoot.resolve(common);
        Path hooksDir = worktreeConfig
            ? gitPath(repoRoot, "sdd2-git-guard/hooks")
            : common.normalize().resolve("sdd2-git-guard/hooks");
        Path metadata = hooksDir.getParent().resolve("routing.json");
        String configured = runGit(
            repoRoot, false, "config", "--path", "--get", "core.hooksPath"
        );
        Path originalDir;
        Path configuredPath = configured.isEmpty() ? null : Paths.get(configured);
        if (configuredPath != null && !configuredPath.isAbsolute()) {
            configuredPath = repoRoot.resolve(configuredPath);
        }
        if (configuredPath != null && configuredPath.normalize().equals(hooksDir)) {
            if (!Files.isRegularFile(metadata)) {
                throw new ControlError("GIT_GUARD_ROUTING_MISSING: " + metadata);
            }
            Map<String, Object> routing = readJson(metadata);
            String originalPath = text(routing, "original_hooks_path");
            if (integer(routing.get("version"), 0) != 2 || blank(originalPath)) {
                throw new ControlError("GIT_GUARD_ROUTING_INVALID: " + metadata);
            }
            originalDir = Paths.get(originalPath);
        } else {
            originalDir = configured.isEmpty()
                ? common.normalize().resolve("hooks") : Paths.get(configured);
            atomicWriteJson(metadata, map(
                "version", 2L, "original_hooks_path", slash(originalDir)
            ));
        }
        Set<String> hookNames = new LinkedHashSet<>(listOf(
            "applypatch-msg", "pre-applypatch", "post-applypatch", "pre-commit",
            "pre-merge-commit", "prepare-commit-msg", "commit-msg", "post-commit",
            "pre-rebase", "post-checkout", "post-merge", "pre-push", "pre-receive",
            "update", "proc-receive", "post-receive", "post-update",
            "reference-transaction", "push-to-checkout", "pre-auto-gc",
            "post-rewrite", "sendemail-validate", "fsmonitor-watchman",
            "p4-changelist", "p4-prepare-changelist", "p4-post-changelist",
            "p4-pre-submit", "post-index-change"
        ));
        Path resolvedOriginal = originalDir.isAbsolute()
            ? originalDir : repoRoot.resolve(originalDir);
        if (resolvedOriginal.normalize().startsWith(hooksDir)) {
            throw new ControlError("GIT_GUARD_ROUTING_CYCLE: " + metadata);
        }
        if (Files.isDirectory(resolvedOriginal)) {
            try (Stream<Path> entries = Files.list(resolvedOriginal)) {
                entries.map(path -> path.getFileName().toString())
                    .filter(name -> name.matches("[A-Za-z0-9._-]+"))
                    .filter(name -> !name.endsWith(".sample")
                        && !name.endsWith(".sdd2-original"))
                    .forEach(hookNames::add);
            } catch (IOException exc) {
                throw new ControlError("Cannot inspect original Git hooks", exc);
            }
        }
        List<String> installed = new ArrayList<>();
        for (String hookName : hookNames) {
            Path hook = hooksDir.resolve(hookName);
            byte[] script = gitGuardScript(hookName, originalDir.resolve(hookName));
            try {
                if (Files.isRegularFile(hook)
                    && Arrays.equals(Files.readAllBytes(hook), script)) {
                    makeExecutable(hook);
                    continue;
                }
                atomicWriteBytes(hook, script);
                makeExecutable(hook);
                if (setOf("prepare-commit-msg", "pre-push").contains(hookName)) {
                    installed.add(hookName);
                }
            } catch (IOException exc) {
                throw new ControlError("Cannot install SDD2 Git guard: " + hook, exc);
            }
        }
        if (!slash(hooksDir).equals(configured)) {
            runGit(repoRoot, "config", configScope, "core.hooksPath", slash(hooksDir));
        }
        if (!gitHooksPath(repoRoot).equals(hooksDir)) {
            throw new ControlError("GIT_GUARD_ROUTING_OVERRIDDEN: core.hooksPath");
        }
        // Migrate the old in-place wrappers only after the new route protects commits.
        for (String hookName : listOf("prepare-commit-msg", "pre-push")) {
            Path legacy = resolvedOriginal.resolve(hookName);
            Path backup = resolvedOriginal.resolve(hookName + ".sdd2-original");
            try {
                if (Files.isRegularFile(legacy)
                    && readUtf8(legacy).contains(COMMIT_GUARD_MARKER)
                    && readUtf8(legacy).contains(hookName + ".sdd2-original")) {
                    if (Files.exists(backup, LinkOption.NOFOLLOW_LINKS)) {
                        Files.move(backup, legacy, StandardCopyOption.REPLACE_EXISTING);
                    } else {
                        Files.delete(legacy);
                    }
                }
            } catch (IOException exc) {
                throw new ControlError("Cannot restore original Git hook: " + legacy, exc);
            }
        }
        return installed;
    }

    static void makeExecutable(Path path) {
        path.toFile().setExecutable(true, false);
        try {
            Files.setPosixFilePermissions(path, setOf(
                PosixFilePermission.OWNER_READ,
                PosixFilePermission.OWNER_WRITE,
                PosixFilePermission.OWNER_EXECUTE,
                PosixFilePermission.GROUP_READ,
                PosixFilePermission.GROUP_EXECUTE,
                PosixFilePermission.OTHERS_READ,
                PosixFilePermission.OTHERS_EXECUTE
            ));
        } catch (UnsupportedOperationException | IOException ignored) {
            // Git for Windows handles hook execution through its bundled shell.
        }
    }

    static String repositoryId(Path repoRoot) {
        List<String> roots = Arrays.stream(
            runGit(repoRoot, "rev-list", "--max-parents=0", "HEAD").split("\\R")
        ).filter(value -> !blank(value)).sorted().collect(Collectors.toList());
        if (roots.isEmpty()) throw new ControlError("Cannot identify Git repository root commit");
        return sha256Bytes(
            canonicalJson(map("root_commits", roots)).getBytes(StandardCharsets.UTF_8)
        );
    }

    static Path stateRepoRoot(Path featureDir, Map<String, Object> state) {
        Path repoRoot = gitRoot(featureDir);
        String expected = text(objectOrEmpty(state.get("workspace_binding")), "repository_id");
        if (expected != null && !expected.equals(repositoryId(repoRoot))) {
            throw new ControlError("Feature state belongs to a different Git repository");
        }
        return repoRoot;
    }

    static Path scopeRepoRoot(Path featureDir, Map<String, Object> scope) {
        Path repoRoot = gitRoot(featureDir);
        String expected = text(scope, "repository_id");
        if (expected != null && !expected.equals(repositoryId(repoRoot))) {
            throw new ControlError("Implementation scope belongs to a different Git repository");
        }
        return repoRoot;
    }

    static Map<String, Path> featurePaths(Path featureDir) {
        Path control = featureDir.resolve(CONTROL_DIR);
        LinkedHashMap<String, Path> result = new LinkedHashMap<>();
        result.put("control", control);
        result.put("state", control.resolve(STATE_FILE));
        result.put("approvals", control.resolve(APPROVAL_FILE));
        result.put("events", control.resolve(EVENT_FILE));
        result.put("scope", control.resolve(SCOPE_FILE));
        result.put("unit_test_evidence", control.resolve(UNIT_TEST_EVIDENCE_FILE));
        result.put("archive_evidence", control.resolve(ARCHIVE_EVIDENCE_FILE));
        result.put("revisions", control.resolve(REVISION_DIR));
        return result;
    }

    static String slash(Path value) {
        return value.toString().replace('\\', '/');
    }

    static String relative(Path root, Path value) {
        return slash(root.relativize(value));
    }

    static List<String> featureLocationErrors(Path repoRoot, Path featureDir) {
        if (!featureDir.startsWith(repoRoot)) {
            return listOf("FEATURE_DIRECTORY_OUTSIDE_REPOSITORY");
        }
        Path relative = repoRoot.relativize(featureDir);
        if (relative.getNameCount() != 3
            || !"sdd2-features".equals(relative.getName(0).toString())) {
            return listOf("FEATURE_DIRECTORY_CONTRACT:" + slash(relative));
        }
        return new ArrayList<>();
    }

    static List<String> featureLayoutErrors(
        Path featureDir, Map<String, Object> state, String allowUnrecordedStage
    ) {
        Set<String> recordedStages = state == null
            ? new LinkedHashSet<>()
            : new LinkedHashSet<>(objectOrEmpty(state.get("artifacts")).keySet());
        Set<String> allowedStages = state == null
            ? new LinkedHashSet<String>(listOf("brief-design"))
            : new LinkedHashSet<>(recordedStages);
        if (state != null) {
            String effectiveAction = text(state, "next_required_action");
            Map<String, Object> block = objectOrEmpty(state.get("blocked"));
            if (FEATURE_LAYOUT_BLOCK.equals(text(block, "code"))) {
                effectiveAction = text(
                    objectOrEmpty(block.get("resume_state")), "next_required_action"
                );
                if (effectiveAction == null) effectiveAction = text(state, "next_required_action");
            }
            String expected = NEXT_ACTION_ARTIFACT_STAGE.get(effectiveAction);
            if (expected != null) allowedStages.add(expected);
        }
        if (allowUnrecordedStage != null) allowedStages.add(allowUnrecordedStage);

        Set<String> allowedDirectories = new LinkedHashSet<>(
            listOf(CONTROL_DIR, CONTROL_DIR + "/" + REVISION_DIR)
        );
        for (String stage : recordedStages) {
            allowedDirectories.add(CONTROL_DIR + "/" + REVISION_DIR + "/" + stage);
        }
        Set<String> allowedControlFiles = ALWAYS_CONTROL_FILENAMES.stream()
            .map(filename -> CONTROL_DIR + "/" + filename)
            .collect(Collectors.toCollection(LinkedHashSet::new));
        if (state != null && state.get("implementation_permit") != null) {
            allowedControlFiles.add(CONTROL_DIR + "/" + SCOPE_FILE);
        }
        if (state != null && state.get("unit_test_execution") != null) {
            allowedControlFiles.add(CONTROL_DIR + "/" + UNIT_TEST_EVIDENCE_FILE);
        }
        if (state != null
            && (recordedStages.contains("archive")
                || "generate-archive-from-evidence".equals(
                    text(state, "next_required_action")
                ))) {
            allowedControlFiles.add(CONTROL_DIR + "/" + ARCHIVE_EVIDENCE_FILE);
        }

        List<String> errors = new ArrayList<>();
        Map<String, List<String>> revisionPaths = new LinkedHashMap<>();
        List<Path> paths;
        try (Stream<Path> walk = Files.walk(featureDir)) {
            paths = walk.filter(path -> !path.equals(featureDir))
                .sorted(Comparator.comparing(path -> slash(featureDir.relativize(path))))
                .collect(Collectors.toList());
        } catch (IOException exc) {
            throw new ControlError("Cannot inspect Feature directory: " + featureDir, exc);
        }
        for (Path path : paths) {
            String rel = relative(featureDir, path);
            if (Files.isSymbolicLink(path)) {
                errors.add("UNEXPECTED_FEATURE_SYMLINK:" + rel);
                continue;
            }
            if (Files.isDirectory(path, LinkOption.NOFOLLOW_LINKS)) {
                if (state == null || !allowedDirectories.contains(rel)) {
                    errors.add("UNEXPECTED_FEATURE_DIRECTORY:" + rel);
                }
                continue;
            }
            if (!Files.isRegularFile(path, LinkOption.NOFOLLOW_LINKS)) {
                errors.add("UNEXPECTED_FEATURE_PATH_TYPE:" + rel);
                continue;
            }
            String stage = ARTIFACT_STAGE_BY_FILENAME.get(rel);
            if (stage != null) {
                if (!allowedStages.contains(stage)) {
                    errors.add("UNEXPECTED_STAGE_ASSET:" + rel);
                }
                continue;
            }
            if (state != null && allowedControlFiles.contains(rel)) continue;
            String filename = rel.contains("/")
                ? rel.substring(rel.lastIndexOf('/') + 1)
                : rel;
            if (state != null && rel.startsWith(CONTROL_DIR + "/")
                && setOf(SCOPE_FILE, UNIT_TEST_EVIDENCE_FILE, ARCHIVE_EVIDENCE_FILE)
                    .contains(filename)) {
                errors.add("UNEXPECTED_CONTROL_FILE:" + rel);
                continue;
            }
            Matcher snapshot = REVISION_SNAPSHOT_PATTERN.matcher(rel);
            if (state != null && snapshot.matches()) {
                stage = snapshot.group(1);
                long revision = Long.parseLong(snapshot.group(2));
                String digest = snapshot.group(3);
                Map<String, Object> artifact = objectOrEmpty(
                    objectOrEmpty(state.get("artifacts")).get(stage)
                );
                long currentRevision = integer(artifact.get("revision"), 0);
                if (!artifact.isEmpty() && revision >= 1 && revision <= currentRevision
                    && sha256File(path).equals(digest)) {
                    String key = stage + "\u0000" + revision;
                    revisionPaths.computeIfAbsent(key, ignored -> new ArrayList<>()).add(rel);
                    continue;
                }
                errors.add("UNEXPECTED_REVISION_SNAPSHOT:" + rel);
                continue;
            }
            errors.add("UNEXPECTED_FEATURE_FILE:" + rel);
        }
        revisionPaths.forEach((key, values) -> {
            if (values.size() > 1) {
                String[] parts = key.split("\\u0000", -1);
                long revision = Long.parseLong(parts[1]);
                for (String path : values) {
                    errors.add(
                        "DUPLICATE_REVISION_SNAPSHOT:" + parts[0] + ":r"
                        + String.format("%04d", revision) + ":" + path
                    );
                }
            }
        });
        return sortedUnique(errors);
    }

    static Path normalizeFeatureDir(String value) {
        Path path = Paths.get(value).toAbsolutePath().normalize();
        if (!Files.isDirectory(path)) {
            throw new ControlError("Feature directory does not exist: " + path);
        }
        try {
            return path.toRealPath();
        } catch (IOException exc) {
            throw new ControlError(
                "Cannot resolve Feature directory: " + path, exc
            );
        }
    }

    static Map<String, Object> loadState(Path featureDir) {
        Map<String, Object> state = readJson(featurePaths(featureDir).get("state"));
        if (!SCHEMA_VERSION.equals(text(state, "schema_version"))) {
            throw new ControlError(
                "Unsupported state schema: " + text(state, "schema_version")
                + "; expected " + SCHEMA_VERSION
            );
        }
        Path repoRoot = gitRoot(featureDir);
        String expected = relative(repoRoot, featureDir);
        if (!expected.equals(text(state, "feature_dir"))) {
            throw new ControlError(
                "Feature directory binding mismatch: state="
                + text(state, "feature_dir") + ", actual=" + expected
            );
        }
        stateRepoRoot(featureDir, state);
        return state;
    }

    static void saveState(Path featureDir, Map<String, Object> state) {
        state.put("updated_at", utcNow());
        atomicWriteJson(featurePaths(featureDir).get("state"), state);
    }

    static String persistArtifactSnapshot(
        Path featureDir, String stage, long revision, String digest
    ) {
        Path source = featureDir.resolve(ARTIFACT_FILES.get(stage));
        Path destination = featurePaths(featureDir).get("revisions")
            .resolve(stage)
            .resolve(String.format("r%04d-%s.md", revision, digest));
        byte[] content;
        try {
            content = Files.readAllBytes(source);
        } catch (IOException exc) {
            throw new ControlError("Cannot snapshot artifact: " + source, exc);
        }
        if (!sha256Bytes(content).equals(digest)) {
            throw new ControlError("Artifact changed while snapshotting: " + source);
        }
        if (Files.exists(destination)) {
            if (!sha256File(destination).equals(digest)) {
                throw new ControlError("Immutable artifact snapshot collision: " + destination);
            }
        } else {
            atomicWriteBytes(destination, content);
        }
        return relative(featureDir, destination);
    }

    static List<Map<String, Object>> readJsonl(Path path) {
        if (!Files.exists(path)) return new ArrayList<>();
        List<Map<String, Object>> records = new ArrayList<>();
        try {
            int lineNumber = 0;
            for (String line : Files.readAllLines(path, StandardCharsets.UTF_8)) {
                lineNumber++;
                if (blank(line)) continue;
                Object value;
                try {
                    value = Json.parse(line);
                } catch (ControlError exc) {
                    throw new ControlError(
                        "Invalid JSONL in " + path + ":" + lineNumber + ": " + exc.getMessage()
                    );
                }
                if (!(value instanceof Map<?, ?>)) {
                    throw new ControlError(
                        "Expected JSON object in " + path + ":" + lineNumber
                    );
                }
                records.add(object(value));
            }
            return records;
        } catch (IOException exc) {
            throw new ControlError("Cannot read JSONL: " + path, exc);
        }
    }

    static List<String> validateHashChain(Path path, String hashField) {
        List<String> errors = new ArrayList<>();
        String previous = null;
        List<Map<String, Object>> records = readJsonl(path);
        for (int index = 0; index < records.size(); index++) {
            Map<String, Object> record = records.get(index);
            String actual = text(record, hashField);
            Map<String, Object> body = new LinkedHashMap<>(record);
            body.remove(hashField);
            String expected = sha256Bytes(
                canonicalJson(body).getBytes(StandardCharsets.UTF_8)
            );
            if (!Objects.equals(actual, expected)) {
                errors.add(path.getFileName() + ":" + (index + 1) + " hash mismatch");
            }
            if (!Objects.equals(body.get("previous_hash"), previous)) {
                errors.add(path.getFileName() + ":" + (index + 1) + " previous_hash mismatch");
            }
            previous = actual;
        }
        return errors;
    }

    static Map<String, Object> appendChainedRecord(
        Path path, Map<String, Object> record, String hashField
    ) {
        List<Map<String, Object>> existing = readJsonl(path);
        Map<String, Object> saved = new LinkedHashMap<>(record);
        saved.put(
            "previous_hash",
            existing.isEmpty() ? null : existing.get(existing.size() - 1).get(hashField)
        );
        saved.put(
            hashField,
            sha256Bytes(canonicalJson(saved).getBytes(StandardCharsets.UTF_8))
        );
        try {
            Files.createDirectories(path.getParent());
            Files.write(
                path, (canonicalJson(saved) + "\n").getBytes(StandardCharsets.UTF_8),
                java.nio.file.StandardOpenOption.CREATE,
                java.nio.file.StandardOpenOption.APPEND
            );
        } catch (IOException exc) {
            throw new ControlError("Cannot append control record: " + path, exc);
        }
        return saved;
    }

    static String stateProjectionSha256(Map<String, Object> state) {
        Map<String, Object> payload = new LinkedHashMap<>(state);
        payload.remove("updated_at");
        return sha256Bytes(canonicalJson(payload).getBytes(StandardCharsets.UTF_8));
    }

    static List<String> stateEventProjectionErrors(
        Path featureDir, Map<String, Object> state
    ) {
        List<Map<String, Object>> events = readJsonl(featurePaths(featureDir).get("events"));
        if (events.isEmpty()) return listOf("STATE_EVENT_HISTORY_MISSING");
        Map<String, Object> latest = events.get(events.size() - 1);
        String expected = text(latest, "state_sha256");
        if (expected == null) return new ArrayList<>();
        List<String> errors = new ArrayList<>();
        if (!expected.equals(stateProjectionSha256(state))) {
            errors.add("STATE_EVENT_PROJECTION_MISMATCH");
        }
        if (!Objects.equals(latest.get("feature_id"), state.get("feature_id"))) {
            errors.add("STATE_EVENT_FEATURE_MISMATCH");
        }
        if (!Objects.equals(latest.get("attempt"), state.get("attempt"))) {
            errors.add("STATE_EVENT_ATTEMPT_MISMATCH");
        }
        if (!Objects.equals(latest.get("revision"), state.get("revision"))) {
            errors.add("STATE_EVENT_REVISION_MISMATCH");
        }
        return errors;
    }

    static void appendEvent(
        Path featureDir, Map<String, Object> state, String eventType,
        Map<String, Object> payload
    ) {
        appendChainedRecord(
            featurePaths(featureDir).get("events"),
            map(
                "event_id", UUID.randomUUID().toString(),
                "timestamp", utcNow(),
                "event_type", eventType,
                "feature_id", state.get("feature_id"),
                "attempt", state.get("attempt"),
                "revision", state.get("revision"),
                "payload", payload,
                "state_sha256", stateProjectionSha256(state)
            ),
            "event_hash"
        );
    }

    static Path lockPath(Path repoRoot) {
        return gitPath(repoRoot, "sdd2-active-feature.json");
    }

    static boolean acquireLock(Path repoRoot, Path featureDir, String featureId) {
        Path path = lockPath(repoRoot);
        String featureRepoPath = relative(repoRoot, featureDir);
        Map<String, Object> record = map(
            "schema_version", SCHEMA_VERSION, "feature_id", featureId,
            "feature_dir", featureRepoPath, "repository_id", repositoryId(repoRoot),
            "acquired_at", utcNow()
        );
        try {
            Files.write(path, (Json.pretty(record) + "\n").getBytes(StandardCharsets.UTF_8),
                StandardOpenOption.CREATE_NEW, StandardOpenOption.WRITE);
            return true;
        } catch (FileAlreadyExistsException exists) {
            Map<String, Object> current = readJson(path);
            if (!featureRepoPath.equals(text(current, "feature_dir"))
                || !featureId.equals(text(current, "feature_id"))
                || !Objects.equals(record.get("repository_id"), current.get("repository_id"))) {
                throw new ControlError(
                    "This Git worktree is locked by another SDD2 feature: "
                    + text(current, "feature_id") + " at " + text(current, "feature_dir")
                    + ". Use a separate Git worktree for parallel features."
                );
            }
            return false;
        } catch (IOException exc) {
            throw new ControlError("Cannot acquire worktree lock: " + path, exc);
        }
    }

    static void releaseLock(Path repoRoot, Path featureDir, String featureId) {
        Path path = lockPath(repoRoot);
        if (!Files.exists(path)) return;
        Map<String, Object> current = readJson(path);
        String featureRepoPath = relative(repoRoot, featureDir);
        if (!featureRepoPath.equals(text(current, "feature_dir"))
            || !featureId.equals(text(current, "feature_id"))) {
            throw new ControlError(
                "Cannot release a worktree lock owned by another SDD2 feature"
            );
        }
        try {
            Files.delete(path);
        } catch (IOException exc) {
            throw new ControlError("Cannot release worktree lock: " + path, exc);
        }
    }

    static void releaseTerminalLock(Path featureDir, Map<String, Object> state) {
        assertHistoryAndLock(featureDir, state);
        Path repoRoot = stateRepoRoot(featureDir, state);
        Path path = lockPath(repoRoot);
        if (!Files.exists(path)) return;
        Map<String, Object> current = readJson(path);
        if (relative(repoRoot, featureDir).equals(text(current, "feature_dir"))
            && Objects.equals(state.get("feature_id"), current.get("feature_id"))
            && repositoryId(repoRoot).equals(text(current, "repository_id"))) {
            installGitGuards(repoRoot);
            releaseLock(repoRoot, featureDir, text(state, "feature_id"));
        }
    }

    static void removeInitializationFiles(Path controlDir) {
        if (!Files.exists(controlDir, LinkOption.NOFOLLOW_LINKS)) return;
        try (Stream<Path> paths = Files.walk(controlDir)) {
            for (Path path : paths.sorted(Comparator.reverseOrder()).collect(Collectors.toList())) {
                Files.delete(path);
            }
        } catch (IOException exc) {
            throw new ControlError("Cannot roll back incomplete initialization: " + controlDir, exc);
        }
    }

    static void recoverIncompleteInitialization(
        Path repoRoot, Path featureDir, String featureId
    ) {
        Path lock = lockPath(repoRoot);
        Map<String, Path> paths = featurePaths(featureDir);
        if (Files.exists(paths.get("state")) || !Files.isRegularFile(lock)) return;
        Map<String, Object> owner = readJson(lock);
        if (!relative(repoRoot, featureDir).equals(text(owner, "feature_dir"))
            || !featureId.equals(text(owner, "feature_id"))
            || !repositoryId(repoRoot).equals(text(owner, "repository_id"))) return;
        Path control = paths.get("control");
        Path brief = featureDir.resolve("brief-design.md");
        String digest = sha256File(brief);
        Path snapshot = control.resolve("revisions/brief-design/r0001-" + digest + ".md");
        Set<Path> allowed = setOf(control, control.resolve("revisions"),
            control.resolve("revisions/brief-design"), snapshot);
        if (Files.exists(control, LinkOption.NOFOLLOW_LINKS)) {
            try (Stream<Path> entries = Files.walk(control)) {
                for (Path path : entries.collect(Collectors.toList())) {
                    if (!allowed.contains(path) || Files.isSymbolicLink(path)) return;
                }
            } catch (IOException exc) {
                throw new ControlError("Cannot inspect incomplete initialization", exc);
            }
            if (Files.exists(snapshot) && !digest.equals(sha256File(snapshot))) return;
        }
        removeInitializationFiles(control);
        releaseLock(repoRoot, featureDir, featureId);
    }

    static List<String> verifyLock(Path featureDir, Map<String, Object> state) {
        if ("historical-example".equals(text(state, "execution_mode"))
            || TERMINAL_STATUSES.contains(text(state, "stage_status"))) {
            return new ArrayList<>();
        }
        Path repoRoot = stateRepoRoot(featureDir, state);
        Path path = lockPath(repoRoot);
        if (!Files.exists(path)) return listOf("FEATURE_LOCK_MISSING");
        Map<String, Object> current = readJson(path);
        if (!Objects.equals(current.get("feature_dir"), state.get("feature_dir"))) {
            return listOf("FEATURE_LOCK_MISMATCH");
        }
        if (!Objects.equals(current.get("feature_id"), state.get("feature_id"))) {
            return listOf("FEATURE_LOCK_ID_MISMATCH");
        }
        if (!Objects.equals(current.get("repository_id"), repositoryId(repoRoot))) {
            return listOf("FEATURE_LOCK_REPOSITORY_MISMATCH");
        }
        return new ArrayList<>();
    }

    static int stageIndex(String stage) {
        String normalized = "unit-test".equals(stage) ? "unit-test-summary" : stage;
        int index = STAGE_ORDER.indexOf(normalized);
        if (index < 0) throw new ControlError("Unknown workflow stage: " + stage);
        return index;
    }

    static List<String> invalidateFrom(
        Map<String, Object> state, String changedStage, String reason
    ) {
        int changedIndex = stageIndex(changedStage);
        List<String> invalidated = new ArrayList<>();
        for (Map.Entry<String, Object> entry
            : objectOrEmpty(state.get("approvals")).entrySet()) {
            Map<String, Object> approval = objectOrEmpty(entry.getValue());
            if ("approved".equals(text(approval, "status"))
                && stageIndex(entry.getKey()) >= changedIndex) {
                approval.put("status", "invalidated");
                approval.put("invalidated_reason", reason);
                invalidated.add("approval:" + entry.getKey());
            }
        }
        Map<String, String> gateStage = linkedMap(
            "code-review", "code-review",
            "auto-fix", "auto-fix",
            "unit-test", "unit-test-summary"
        );
        for (Map.Entry<String, Object> entry
            : objectOrEmpty(state.get("quality_gates")).entrySet()) {
            Map<String, Object> result = objectOrEmpty(entry.getValue());
            if (!setOf("invalidated", "not-recorded").contains(text(result, "status"))
                && stageIndex(gateStage.get(entry.getKey())) >= changedIndex) {
                result.put("status", "invalidated");
                result.put("invalidated_reason", reason);
                invalidated.add("quality:" + entry.getKey());
            }
        }
        for (Map.Entry<String, Object> entry
            : objectOrEmpty(state.get("phase_reviews")).entrySet()) {
            Map<String, Object> review = objectOrEmpty(entry.getValue());
            if (changedIndex <= stageIndex("tasks")
                && "approved".equals(text(review, "status"))) {
                review.put("status", "invalidated");
                review.put("invalidated_reason", reason);
                invalidated.add("phase:" + entry.getKey());
            }
        }
        if (!invalidated.isEmpty()) {
            arrayOrEmptyPut(state, "invalidations", map(
                "timestamp", utcNow(),
                "changed_stage", changedStage,
                "reason", reason,
                "invalidated", invalidated
            ));
        }
        return invalidated;
    }

    static void arrayOrEmptyPut(Map<String, Object> map, String key, Object value) {
        List<Object> values;
        if (map.get(key) instanceof List<?>) {
            values = arrayOrEmpty(map.get(key));
        } else {
            values = new ArrayList<>();
            map.put(key, values);
        }
        values.add(value);
    }

    static boolean containsAny(String value, Collection<String> terms) {
        for (String term : terms) if (value.contains(term)) return true;
        return false;
    }

    static boolean directApproval(String value, Collection<String> stageTerms) {
        String lowered = value.trim().toLowerCase(Locale.ROOT);
        List<String> rejected = new ArrayList<>(APPROVAL_REJECTION_TERMS);
        rejected.addAll(APPROVAL_META_TERMS);
        if (containsAny(lowered, rejected)) return false;
        return APPROVAL_PATTERN.matcher(lowered).find()
            && stageTerms.stream().anyMatch(
                term -> lowered.contains(term.toLowerCase(Locale.ROOT))
            );
    }

    static boolean explicitApproval(String stage, String value) {
        return directApproval(value, STAGE_WORDS.get(stage));
    }

    static List<String> uniqueInOrder(Collection<String> values) {
        return new ArrayList<>(new LinkedHashSet<>(values));
    }

    static String currentArtifactHash(Path featureDir, String stage) {
        String filename = ARTIFACT_FILES.get(stage);
        if (filename == null) throw new ControlError("Unknown artifact stage: " + stage);
        return sha256File(featureDir.resolve(filename));
    }

    static List<String> artifactDrift(Path featureDir, Map<String, Object> state) {
        List<String> errors = new ArrayList<>();
        for (Map.Entry<String, Object> entry
            : objectOrEmpty(state.get("artifacts")).entrySet()) {
            String stage = entry.getKey();
            Map<String, Object> record = objectOrEmpty(entry.getValue());
            Path path = featureDir.resolve(text(record, "path"));
            if (!Files.isRegularFile(path, LinkOption.NOFOLLOW_LINKS)) {
                errors.add("ARTIFACT_MISSING:" + stage + ":" + text(record, "path"));
                continue;
            }
            String actual = sha256File(path);
            if (!Objects.equals(actual, record.get("sha256"))) {
                errors.add("ARTIFACT_DRIFT:" + stage + ":" + text(record, "path"));
            }
            String snapshotPath = text(record, "snapshot_path");
            if (snapshotPath == null) {
                if (!"historical-example".equals(text(state, "execution_mode"))) {
                    errors.add("ARTIFACT_SNAPSHOT_MISSING:" + stage);
                }
                continue;
            }
            Path snapshot = featureDir.resolve(snapshotPath);
            if (!Files.isRegularFile(snapshot, LinkOption.NOFOLLOW_LINKS)) {
                errors.add(
                    "ARTIFACT_SNAPSHOT_FILE_MISSING:" + stage + ":" + snapshotPath
                );
            } else if (!Objects.equals(sha256File(snapshot), record.get("sha256"))) {
                errors.add("ARTIFACT_SNAPSHOT_DRIFT:" + stage + ":" + snapshotPath);
            }
        }
        return errors;
    }

    static List<String> splitNullSeparated(String value) {
        return Arrays.stream(value.split("\u0000", -1))
            .filter(item -> !item.isEmpty())
            .collect(Collectors.toList());
    }

    static List<String> changedPaths(Path repoRoot, String baseCommit) {
        Set<String> paths = new TreeSet<>();
        paths.addAll(splitNullSeparated(
            runGit(repoRoot, "diff", "--name-only", "-z", baseCommit)
        ));
        paths.addAll(splitNullSeparated(
            runGit(repoRoot, "ls-files", "--others", "--exclude-standard", "-z")
        ));
        return new ArrayList<>(paths);
    }

    static List<String> uncontrolledSiblingFeatureErrors(
        Path repoRoot, String featureRepoPath
    ) {
        String headCommit = runGit(repoRoot, "rev-parse", "HEAD");
        String currentPrefix = featureRepoPath.replaceAll("/+$", "") + "/";
        String activeFeatureDir = null;
        Path currentLock = lockPath(repoRoot);
        if (Files.isRegularFile(currentLock)) {
            try {
                activeFeatureDir = text(readJson(currentLock), "feature_dir");
            } catch (ControlError ignored) {
                activeFeatureDir = null;
            }
        }
        Set<String> siblingRoots = new TreeSet<>();
        for (String rel : changedPaths(repoRoot, headCommit)) {
            if (rel.equals(featureRepoPath) || rel.startsWith(currentPrefix)) continue;
            String[] parts = rel.split("/");
            if (parts.length < 3 || !"sdd2-features".equals(parts[0])) continue;
            siblingRoots.add(String.join("/", Arrays.copyOfRange(parts, 0, 3)));
        }
        List<String> errors = new ArrayList<>();
        for (String siblingRoot : siblingRoots) {
            if (siblingRoot.equals(activeFeatureDir)) continue;
            Path siblingStatePath = repoRoot.resolve(siblingRoot)
                .resolve(CONTROL_DIR).resolve(STATE_FILE);
            Map<String, Object> siblingState = null;
            try {
                siblingState = readJson(siblingStatePath);
            } catch (ControlError ignored) {
                // An uninitialized changed Feature is still uncontrolled.
            }
            if (siblingState != null
                && TERMINAL_STATUSES.contains(text(siblingState, "stage_status"))) continue;
            errors.add("UNCONTROLLED_SIBLING_FEATURE:" + siblingRoot);
        }
        return errors;
    }

    static List<String> featureGenerationErrors(
        Path featureDir, Map<String, Object> state, String allowUnrecordedStage
    ) {
        if ("historical-example".equals(text(state, "execution_mode"))) {
            return new ArrayList<>();
        }
        Path repoRoot = stateRepoRoot(featureDir, state);
        List<String> errors = new ArrayList<>(featureLocationErrors(repoRoot, featureDir));
        errors.addAll(featureLayoutErrors(featureDir, state, allowUnrecordedStage));
        errors.addAll(uncontrolledSiblingFeatureErrors(
            repoRoot, text(state, "feature_repo_path")
        ));
        return sortedUnique(errors);
    }

    static Map<String, Object> planningSnapshot(Path repoRoot, String featureRepoPath) {
        String headCommit = runGit(repoRoot, "rev-parse", "HEAD");
        String featurePrefix = featureRepoPath.replaceAll("/+$", "") + "/";
        List<Object> files = new ArrayList<>();
        for (String rel : changedPaths(repoRoot, headCommit)) {
            if (rel.equals(featureRepoPath) || rel.startsWith(featurePrefix)) continue;
            Path path = repoRoot.resolve(rel);
            files.add(map(
                "path", rel,
                "sha256", Files.isRegularFile(path) ? sha256File(path) : "<deleted>"
            ));
        }
        Map<String, Object> payload = map(
            "branch", runGit(repoRoot, "branch", "--show-current"),
            "head_commit", headCommit,
            "head_tree", runGit(repoRoot, "rev-parse", "HEAD^{tree}"),
            "files", files
        );
        Map<String, Object> result = new LinkedHashMap<>();
        result.put("captured_at", utcNow());
        result.putAll(payload);
        result.put(
            "snapshot_sha256",
            sha256Bytes(canonicalJson(payload).getBytes(StandardCharsets.UTF_8))
        );
        return result;
    }

    static List<String> planningGuardErrors(
        Path featureDir, Map<String, Object> state
    ) {
        if ("historical-example".equals(text(state, "execution_mode"))
            || TERMINAL_STATUSES.contains(text(state, "stage_status"))
            || truth(state.get("implementation_started"))
            || state.get("implementation_permit") != null) {
            return new ArrayList<>();
        }
        if (!(state.get("planning_baseline") instanceof Map<?, ?>)) {
            return listOf("PLANNING_BASELINE_MISSING");
        }
        Map<String, Object> baseline = object(state.get("planning_baseline"));
        Map<String, Object> current = planningSnapshot(
            stateRepoRoot(featureDir, state), text(state, "feature_repo_path")
        );
        List<String> errors = new ArrayList<>();
        if (!Objects.equals(current.get("branch"), baseline.get("branch"))) {
            String currentBranch = text(current, "branch");
            errors.add(
                "PRE_IMPLEMENTATION_BRANCH_CHANGE:" + text(baseline, "branch")
                + "->" + (currentBranch == null || currentBranch.isEmpty()
                    ? "<detached>" : currentBranch)
            );
        }
        if (!Objects.equals(current.get("head_commit"), baseline.get("head_commit"))) {
            errors.add(
                "PRE_IMPLEMENTATION_GIT_HEAD_CHANGE:" + text(baseline, "head_commit")
                + "->" + text(current, "head_commit")
            );
        }
        Map<String, String> baselineFiles = fileDigestMap(baseline.get("files"));
        Map<String, String> currentFiles = fileDigestMap(current.get("files"));
        TreeSet<String> paths = new TreeSet<>(baselineFiles.keySet());
        paths.addAll(currentFiles.keySet());
        for (String path : paths) {
            if (!Objects.equals(baselineFiles.get(path), currentFiles.get(path))) {
                errors.add("PRE_IMPLEMENTATION_CHANGE:" + path);
            }
        }
        if (errors.isEmpty()
            && !Objects.equals(
                current.get("snapshot_sha256"), baseline.get("snapshot_sha256")
            )) {
            errors.add("PRE_IMPLEMENTATION_SNAPSHOT_MISMATCH");
        }
        return errors;
    }

    static Map<String, String> fileDigestMap(Object value) {
        LinkedHashMap<String, String> result = new LinkedHashMap<>();
        for (Object item : arrayOrEmpty(value)) {
            Map<String, Object> record = objectOrEmpty(item);
            result.put(text(record, "path"), text(record, "sha256"));
        }
        return result;
    }

    static void blockPrematureImplementationChange(
        Path featureDir, Map<String, Object> state, List<String> errors
    ) {
        Map<String, Object> currentBlock = objectOrEmpty(state.get("blocked"));
        if (PREMATURE_CHANGE_BLOCK.equals(text(currentBlock, "code"))) return;
        Map<String, Object> resumeState = map(
            "current_stage", state.get("current_stage"),
            "stage_status", state.get("stage_status"),
            "next_required_action", state.get("next_required_action")
        );
        state.put("blocked", map(
            "code", PREMATURE_CHANGE_BLOCK,
            "reason", String.join(", ", errors),
            "recovery", "撤销或移走所有提前产生的代码、测试、配置和 Git 提交，然后再次恢复当前 Gate。",
            "resume_state", resumeState
        ));
        state.put("stage_status", "blocked");
        state.put(
            "next_required_action", "restore-planning-baseline-before-current-gate"
        );
        incrementRevision(state);
        appendEvent(
            featureDir, state, "premature-implementation-blocked",
            map("errors", errors, "resume_state", resumeState)
        );
        saveState(featureDir, state);
    }

    static void restorePrematureChangeBlock(
        Path featureDir, Map<String, Object> state
    ) {
        Map<String, Object> block = objectOrEmpty(state.get("blocked"));
        if (!PREMATURE_CHANGE_BLOCK.equals(text(block, "code"))) return;
        Map<String, Object> resumeState = objectOrEmpty(block.get("resume_state"));
        if (!resumeState.keySet().containsAll(
            setOf("current_stage", "stage_status", "next_required_action")
        )) {
            throw new ControlError("PREMATURE_IMPLEMENTATION_BLOCK_RESUME_STATE_MISSING");
        }
        state.put("current_stage", resumeState.get("current_stage"));
        state.put("stage_status", resumeState.get("stage_status"));
        state.put("next_required_action", resumeState.get("next_required_action"));
        state.put("blocked", null);
        incrementRevision(state);
        appendEvent(
            featureDir, state, "premature-implementation-restored",
            map("restored", resumeState)
        );
        saveState(featureDir, state);
    }

    static void blockUnexpectedFeatureLayout(
        Path featureDir, Map<String, Object> state, List<String> errors
    ) {
        Map<String, Object> currentBlock = objectOrEmpty(state.get("blocked"));
        if (FEATURE_LAYOUT_BLOCK.equals(text(currentBlock, "code"))) return;
        Map<String, Object> resumeState = map(
            "current_stage", state.get("current_stage"),
            "stage_status", state.get("stage_status"),
            "next_required_action", state.get("next_required_action"),
            "blocked", state.get("blocked")
        );
        state.put("blocked", map(
            "code", FEATURE_LAYOUT_BLOCK,
            "reason", String.join(", ", errors),
            "recovery", "移走或删除白名单外文件及重复 Feature 目录，然后再次恢复；不得把额外文件追认为流程资产。",
            "resume_state", resumeState
        ));
        state.put("stage_status", "blocked");
        state.put(
            "next_required_action", "remove-unexpected-feature-paths-before-current-action"
        );
        incrementRevision(state);
        appendEvent(
            featureDir, state, "unexpected-feature-layout-blocked",
            map("errors", errors, "resume_state", resumeState)
        );
        saveState(featureDir, state);
    }

    static void restoreUnexpectedFeatureLayoutBlock(
        Path featureDir, Map<String, Object> state
    ) {
        Map<String, Object> block = objectOrEmpty(state.get("blocked"));
        if (!FEATURE_LAYOUT_BLOCK.equals(text(block, "code"))) return;
        Map<String, Object> resumeState = objectOrEmpty(block.get("resume_state"));
        if (!resumeState.keySet().containsAll(
            setOf("current_stage", "stage_status", "next_required_action", "blocked")
        )) {
            throw new ControlError("UNEXPECTED_FEATURE_LAYOUT_RESUME_STATE_MISSING");
        }
        state.put("current_stage", resumeState.get("current_stage"));
        state.put("stage_status", resumeState.get("stage_status"));
        state.put("next_required_action", resumeState.get("next_required_action"));
        state.put("blocked", resumeState.get("blocked"));
        incrementRevision(state);
        appendEvent(
            featureDir, state, "unexpected-feature-layout-restored",
            map("restored", resumeState)
        );
        saveState(featureDir, state);
    }

    static void incrementRevision(Map<String, Object> state) {
        state.put("revision", integer(state.get("revision"), 0) + 1);
    }

    static boolean pathMatches(String path, Collection<String> patterns) {
        for (String pattern : patterns) {
            if (path.equals(pattern) || fnmatch(path, pattern)) return true;
        }
        return false;
    }

    static boolean fnmatch(String value, String pattern) {
        StringBuilder regex = new StringBuilder("^");
        for (int index = 0; index < pattern.length(); index++) {
            char current = pattern.charAt(index);
            if (current == '*') {
                regex.append(".*");
            } else if (current == '?') {
                regex.append('.');
            } else if (current == '[') {
                int end = pattern.indexOf(']', index + 1);
                if (end < 0) {
                    regex.append("\\[");
                } else {
                    String content = pattern.substring(index + 1, end);
                    if (content.startsWith("!")) content = "^" + content.substring(1);
                    regex.append('[').append(content).append(']');
                    index = end;
                }
            } else {
                if ("\\.^$|(){}+".indexOf(current) >= 0) regex.append('\\');
                regex.append(current);
            }
        }
        regex.append('$');
        return Pattern.compile(regex.toString()).matcher(value).matches();
    }

    static void rejectUnsafePatterns(Collection<String> patterns) {
        Set<String> unsafe = setOf("", ".", "./", "*", "**", "**/*", "/");
        List<String> bad = patterns.stream()
            .filter(pattern ->
                unsafe.contains(pattern.trim()) || Paths.get(pattern).isAbsolute()
            )
            .collect(Collectors.toList());
        if (!bad.isEmpty()) {
            throw new ControlError(
                "Unsafe or overly broad scope pattern(s): " + String.join(", ", bad)
            );
        }
    }

    static List<String> sortedUnique(Collection<String> values) {
        return new ArrayList<>(new TreeSet<>(values));
    }

    static Map<String, Object> snapshotForScope(
        Path repoRoot, Map<String, Object> scope
    ) {
        String baseCommit = text(scope, "base_commit");
        String featureRepoPath = text(scope, "feature_repo_path");
        String featurePrefix = featureRepoPath.replaceAll("/+$", "") + "/";
        List<Object> files = new ArrayList<Object>();
        List<String> violations = new ArrayList<String>();
        String currentBranch = runGit(repoRoot, "branch", "--show-current");
        if (!Objects.equals(currentBranch, scope.get("branch"))) {
            violations.add(
                "BRANCH_MISMATCH:" + (blank(currentBranch) ? "<detached>" : currentBranch)
            );
        }
        List<String> forbidden = stringList(scope.get("forbidden_paths"));
        List<String> allowed = stringList(scope.get("allowed_paths"));
        for (String rel : changedPaths(repoRoot, baseCommit)) {
            if (rel.equals(featureRepoPath) || rel.startsWith(featurePrefix)) continue;
            if (pathMatches(rel, forbidden)) {
                violations.add("FORBIDDEN_PATH:" + rel);
                continue;
            }
            if (!pathMatches(rel, allowed)) {
                violations.add("OUT_OF_SCOPE:" + rel);
                continue;
            }
            Path path = repoRoot.resolve(rel);
            files.add(map(
                "path", rel,
                "sha256", Files.isRegularFile(path) ? sha256File(path) : "<deleted>"
            ));
        }
        Map<String, Object> payload = map(
            "base_commit", baseCommit,
            "branch", scope.get("branch"),
            "head_commit", runGit(repoRoot, "rev-parse", "HEAD"),
            "head_tree", runGit(repoRoot, "rev-parse", "HEAD^{tree}"),
            "files", files
        );
        return map(
            "captured_at", utcNow(),
            "files", files,
            "head_commit", payload.get("head_commit"),
            "head_tree", payload.get("head_tree"),
            "snapshot_sha256",
            sha256Bytes(canonicalJson(payload).getBytes(StandardCharsets.UTF_8)),
            "violations", violations
        );
    }

    static List<String> changedTestPaths(
        Map<String, Object> scope, Map<String, Object> snapshot
    ) {
        List<String> patterns = stringList(scope.get("test_path_patterns"));
        if (patterns.isEmpty()) patterns = new ArrayList<String>(DEFAULT_TEST_PATHS);
        List<String> result = new ArrayList<String>();
        for (Object value : arrayOrEmpty(snapshot.get("files"))) {
            Map<String, Object> item = objectOrEmpty(value);
            String path = text(item, "path");
            if (!"<deleted>".equals(text(item, "sha256"))
                && pathMatches(path, patterns)) {
                result.add(path);
            }
        }
        Collections.sort(result);
        return result;
    }

    static String executableName(String value) {
        String normalized = value.replace('\\', '/');
        int slash = normalized.lastIndexOf('/');
        return (slash >= 0 ? normalized.substring(slash + 1) : normalized)
            .toLowerCase(Locale.ROOT);
    }

    static String testCommandKind(List<String> command) {
        if (command.isEmpty()) {
            throw new ControlError(
                "Unit Test execution requires a test command after --"
            );
        }
        for (String value : command) {
            if (value.indexOf('\u0000') >= 0 || value.indexOf('\n') >= 0) {
                throw new ControlError("Unit Test command contains an invalid argument");
            }
        }
        String executable = executableName(command.get(0));
        List<String> arguments = new ArrayList<String>();
        for (int index = 1; index < command.size(); index++) {
            arguments.add(command.get(index).toLowerCase(Locale.ROOT));
        }
        if (executable.startsWith("python")) {
            if (arguments.size() >= 2 && "-m".equals(arguments.get(0))
                && setOf("unittest", "pytest").contains(arguments.get(1))) {
                return "python-" + arguments.get(1);
            }
        } else if (setOf("pytest", "py.test").contains(executable)) {
            return "pytest";
        } else if (setOf("mvn", "mvnw", "mvnw.cmd").contains(executable)) {
            boolean skipped = false;
            for (String value : arguments) {
                if ("-dskiptests".equals(value)
                    || "-dmaven.test.skip=true".equals(value)
                    || value.startsWith("-dskiptests=")) {
                    skipped = true;
                }
            }
            if (arguments.contains("test") && !skipped) return "maven-test";
        } else if (setOf("gradle", "gradlew", "gradlew.bat").contains(executable)) {
            boolean hasTest = false;
            boolean skipped = false;
            for (int index = 0; index < arguments.size(); index++) {
                String value = arguments.get(index);
                if ("test".equals(value) || value.endsWith(":test")) hasTest = true;
                if ("-x".equals(value) && index + 1 < arguments.size()
                    && "test".equals(arguments.get(index + 1))) skipped = true;
            }
            if (hasTest && !skipped) return "gradle-test";
        } else if (setOf("npm", "pnpm", "yarn", "bun").contains(executable)) {
            if (arguments.contains("test")) return executable + "-test";
        } else if ("dotnet".equals(executable)
            && !arguments.isEmpty() && "test".equals(arguments.get(0))) {
            return "dotnet-test";
        } else if ("go".equals(executable)
            && !arguments.isEmpty() && "test".equals(arguments.get(0))) {
            return "go-test";
        } else if ("cargo".equals(executable)
            && !arguments.isEmpty() && "test".equals(arguments.get(0))) {
            return "cargo-test";
        }
        throw new ControlError(
            "Unsupported or non-test command. Use a recognized test runner "
            + "without shell wrappers or skip-test flags."
        );
    }

    static List<Matcher> allMatches(Pattern pattern, String value) {
        List<Matcher> result = new ArrayList<Matcher>();
        Matcher source = pattern.matcher(value);
        while (source.find()) {
            Matcher copy = pattern.matcher(source.group());
            if (copy.find()) result.add(copy);
        }
        return result;
    }

    static Map<String, Object> testCounts(
        long total, long passed, long failed, long errors, long skipped, String source
    ) {
        return map(
            "total", total,
            "passed", passed,
            "failed", failed,
            "errors", errors,
            "skipped", skipped,
            "source", source
        );
    }

    static Map<String, Object> parsedTestCounts(String stdout, String stderr) {
        String output = stdout + "\n" + stderr;
        Pattern mavenPattern = Pattern.compile(
            "Tests run:\\s*(\\d+),\\s*Failures:\\s*(\\d+),\\s*Errors:\\s*(\\d+),"
            + "\\s*Skipped:\\s*(\\d+)",
            Pattern.CASE_INSENSITIVE
        );
        Matcher maven = mavenPattern.matcher(output);
        long[] lastMaven = null;
        while (maven.find()) {
            lastMaven = new long[] {
                Long.parseLong(maven.group(1)), Long.parseLong(maven.group(2)),
                Long.parseLong(maven.group(3)), Long.parseLong(maven.group(4))
            };
        }
        if (lastMaven != null) {
            long passed = Math.max(
                0, lastMaven[0] - lastMaven[1] - lastMaven[2] - lastMaven[3]
            );
            return testCounts(
                lastMaven[0], passed, lastMaven[1], lastMaven[2], lastMaven[3],
                "maven-surefire-output"
            );
        }

        Matcher unittest = Pattern.compile(
            "Ran\\s+(\\d+)\\s+tests?", Pattern.CASE_INSENSITIVE
        ).matcher(output);
        if (unittest.find()) {
            long total = Long.parseLong(unittest.group(1));
            long failed = 0;
            long errors = 0;
            long skipped = 0;
            Matcher failedSummary = Pattern.compile(
                "FAILED\\s*\\(([^)]*)\\)", Pattern.CASE_INSENSITIVE
            ).matcher(output);
            if (failedSummary.find()) {
                Matcher values = Pattern.compile(
                    "(failures|errors|skipped)\\s*=\\s*(\\d+)",
                    Pattern.CASE_INSENSITIVE
                ).matcher(failedSummary.group(1));
                while (values.find()) {
                    String label = values.group(1).toLowerCase(Locale.ROOT);
                    long count = Long.parseLong(values.group(2));
                    if ("failures".equals(label)) failed = count;
                    if ("errors".equals(label)) errors = count;
                    if ("skipped".equals(label)) skipped = count;
                }
            } else {
                Matcher skippedSummary = Pattern.compile(
                    "OK\\s*\\(\\s*skipped\\s*=\\s*(\\d+)\\s*\\)",
                    Pattern.CASE_INSENSITIVE
                ).matcher(output);
                if (skippedSummary.find()) {
                    skipped = Long.parseLong(skippedSummary.group(1));
                }
            }
            return testCounts(
                total, Math.max(0, total - failed - errors - skipped),
                failed, errors, skipped, "python-unittest-output"
            );
        }

        String[] lines = output.split("\\R");
        Pattern pytestTerm = Pattern.compile(
            "\\b(?:passed|failed|error|errors|skipped)\\b",
            Pattern.CASE_INSENSITIVE
        );
        String pytestSummary = null;
        for (String line : lines) {
            if (pytestTerm.matcher(line).find()) pytestSummary = line;
        }
        if (pytestSummary != null) {
            long passed = 0;
            long failed = 0;
            long errors = 0;
            long skipped = 0;
            boolean found = false;
            Matcher values = Pattern.compile(
                "(\\d+)\\s+(passed|failed|errors?|skipped)",
                Pattern.CASE_INSENSITIVE
            ).matcher(pytestSummary);
            while (values.find()) {
                found = true;
                long count = Long.parseLong(values.group(1));
                String label = values.group(2).toLowerCase(Locale.ROOT);
                if ("passed".equals(label)) passed = count;
                if ("failed".equals(label)) failed = count;
                if ("error".equals(label) || "errors".equals(label)) errors += count;
                if ("skipped".equals(label)) skipped = count;
            }
            if (found) {
                return testCounts(
                    passed + failed + errors + skipped, passed, failed, errors,
                    skipped, "pytest-output"
                );
            }
        }

        Matcher cargo = Pattern.compile(
            "test result:\\s*\\w+\\.\\s*(\\d+)\\s+passed;\\s*(\\d+)\\s+failed;"
            + "\\s*(\\d+)\\s+ignored",
            Pattern.CASE_INSENSITIVE
        ).matcher(output);
        long cargoPassed = 0;
        long cargoFailed = 0;
        long cargoSkipped = 0;
        boolean cargoFound = false;
        while (cargo.find()) {
            cargoFound = true;
            cargoPassed += Long.parseLong(cargo.group(1));
            cargoFailed += Long.parseLong(cargo.group(2));
            cargoSkipped += Long.parseLong(cargo.group(3));
        }
        if (cargoFound) {
            return testCounts(
                cargoPassed + cargoFailed + cargoSkipped, cargoPassed, cargoFailed,
                0, cargoSkipped, "cargo-output"
            );
        }

        Matcher jest = Pattern.compile(
            "Tests:\\s*(?:(\\d+)\\s+failed,\\s*)?"
            + "(?:(\\d+)\\s+skipped,\\s*)?(\\d+)\\s+passed,\\s*(\\d+)\\s+total",
            Pattern.CASE_INSENSITIVE
        ).matcher(output);
        long[] lastJest = null;
        while (jest.find()) {
            lastJest = new long[] {
                jest.group(1) == null ? 0 : Long.parseLong(jest.group(1)),
                jest.group(2) == null ? 0 : Long.parseLong(jest.group(2)),
                Long.parseLong(jest.group(3)), Long.parseLong(jest.group(4))
            };
        }
        if (lastJest != null) {
            return testCounts(
                lastJest[3], lastJest[2], lastJest[0], 0, lastJest[1], "jest-output"
            );
        }
        return testCounts(0, 0, 0, 0, 0, "unverified");
    }

    static String boundedOutput(String value, int limit) {
        if (value.length() <= limit) return value;
        int half = limit / 2;
        return value.substring(0, half)
            + "\n...[output truncated by SDD2 controller]...\n"
            + value.substring(value.length() - half);
    }

    static Map<String, Object> loadScope(Path featureDir) {
        return readJson(featurePaths(featureDir).get("scope"));
    }

    static List<String> unitTestExecutionErrors(
        Path featureDir, Map<String, Object> state, String requiredOutcome
    ) {
        if (!(state.get("unit_test_execution") instanceof Map<?, ?>)) {
            return listOf("UNIT_TEST_EXECUTION_MISSING");
        }
        Map<String, Object> projection = object(state.get("unit_test_execution"));
        Path path = featurePaths(featureDir).get("unit_test_evidence");
        if (!Files.isRegularFile(path)) {
            return listOf("UNIT_TEST_EVIDENCE_FILE_MISSING");
        }
        Map<String, Object> evidence;
        try {
            evidence = readJson(path);
        } catch (ControlError exc) {
            return listOf("UNIT_TEST_EVIDENCE_INVALID");
        }
        Map<String, Object> body = new LinkedHashMap<String, Object>(evidence);
        Object actualHash = body.remove("evidence_sha256");
        String expectedHash = sha256Bytes(
            canonicalJson(body).getBytes(StandardCharsets.UTF_8)
        );
        List<String> errors = new ArrayList<String>();
        if (!Objects.equals(actualHash, expectedHash)) {
            errors.add("UNIT_TEST_EVIDENCE_HASH_MISMATCH");
        }
        Map<String, Object> expected = map(
            "feature_id", state.get("feature_id"),
            "attempt", state.get("attempt"),
            "evidence_sha256", actualHash,
            "scope_sha256", evidence.get("scope_sha256"),
            "code_revision", evidence.get("code_revision"),
            "outcome", evidence.get("outcome")
        );
        for (Map.Entry<String, Object> entry : expected.entrySet()) {
            if (!Objects.equals(projection.get(entry.getKey()), entry.getValue())) {
                errors.add("UNIT_TEST_STATE_EVIDENCE_MISMATCH:" + entry.getKey());
            }
        }
        try {
            Map<String, Object> scope = loadScope(featureDir);
            Map<String, Object> frozen = objectOrEmpty(scope.get("frozen_snapshot"));
            List<String> expectedPaths = changedTestPaths(scope, frozen);
            List<Object> expectedSources = new ArrayList<Object>();
            for (Object item : arrayOrEmpty(frozen.get("files"))) {
                Map<String, Object> source = objectOrEmpty(item);
                if (expectedPaths.contains(text(source, "path"))) {
                    expectedSources.add(item);
                }
            }
            if (!Objects.equals(evidence.get("scope_sha256"), frozen.get("snapshot_sha256"))) {
                errors.add("UNIT_TEST_EVIDENCE_SCOPE_MISMATCH");
            }
            if (!Objects.equals(evidence.get("changed_test_paths"), expectedPaths)) {
                errors.add("UNIT_TEST_EVIDENCE_TEST_PATH_MISMATCH");
            }
            if (!Objects.equals(evidence.get("changed_test_sources"), expectedSources)) {
                errors.add("UNIT_TEST_EVIDENCE_TEST_SOURCE_HASH_MISMATCH");
            }
        } catch (RuntimeException exc) {
            errors.add("UNIT_TEST_EVIDENCE_SCOPE_INVALID");
        }
        if (requiredOutcome != null
            && !requiredOutcome.equals(text(evidence, "outcome"))) {
            errors.add(
                "UNIT_TEST_OBSERVED_OUTCOME_MISMATCH:" + text(evidence, "outcome")
                + "!=" + requiredOutcome
            );
        }
        Map<String, Object> counts = objectOrEmpty(evidence.get("test_counts"));
        if (counts.isEmpty()) errors.add("UNIT_TEST_COUNTS_MISSING");
        if ("passed".equals(text(evidence, "outcome"))) {
            if (integer(evidence.get("exit_code"), Long.MIN_VALUE) != 0) {
                errors.add("UNIT_TEST_PASSED_WITH_NONZERO_EXIT");
            }
            if (integer(counts.get("total"), 0) <= 0
                || integer(counts.get("passed"), 0) <= 0) {
                errors.add("UNIT_TEST_PASSED_WITHOUT_OBSERVED_TEST");
            }
            if (integer(counts.get("failed"), 0) != 0
                || integer(counts.get("errors"), 0) != 0) {
                errors.add("UNIT_TEST_PASSED_WITH_FAILURES");
            }
            if (!Boolean.FALSE.equals(evidence.get("scope_changed_during_test"))) {
                errors.add("UNIT_TEST_PASSED_WITH_SCOPE_CHANGE");
            }
        }
        return errors;
    }

    static List<String> scopeDrift(Path featureDir, Map<String, Object> state) {
        Path scopePath = featurePaths(featureDir).get("scope");
        if (!Files.exists(scopePath)) {
            if (TERMINAL_STATUSES.contains(text(state, "stage_status"))
                && !"completed".equals(text(state, "stage_status"))) {
                return new ArrayList<String>();
            }
            if (stageIndex(text(state, "current_stage")) >= stageIndex("implementation")
                && !"capture-implementation-scope".equals(
                    text(state, "next_required_action")
                )) {
                return listOf("SCOPE_MANIFEST_MISSING");
            }
            return new ArrayList<String>();
        }
        try {
            Map<String, Object> scope = loadScope(featureDir);
            Map<String, Object> snapshot = snapshotForScope(
                scopeRepoRoot(featureDir, scope), scope
            );
            List<String> violations = stringList(snapshot.get("violations"));
            if (!violations.isEmpty()) return violations;
            Map<String, Object> frozen = objectOrEmpty(scope.get("frozen_snapshot"));
            if (!frozen.isEmpty()
                && !Objects.equals(
                    frozen.get("snapshot_sha256"), snapshot.get("snapshot_sha256")
                )) {
                return listOf("IMPLEMENTATION_SCOPE_DRIFT");
            }
            return new ArrayList<String>();
        } catch (RuntimeException exc) {
            return listOf("SCOPE_MANIFEST_INVALID");
        }
    }

    static List<String> approvalRecordBindingErrors(
        Path featureDir, Map<String, Object> state, String stage,
        Map<String, Object> approval
    ) {
        Object approvalId = approval.get("approval_id");
        List<Map<String, Object>> matches = new ArrayList<Map<String, Object>>();
        for (Map<String, Object> record
            : readJsonl(featurePaths(featureDir).get("approvals"))) {
            if (Objects.equals(record.get("approval_id"), approvalId)) matches.add(record);
        }
        if (matches.size() != 1) {
            return listOf(
                "APPROVAL_CHAIN_RECORD_" + (matches.isEmpty() ? "MISSING" : "DUPLICATED")
                + ":" + stage
            );
        }
        Map<String, Object> record = matches.get(0);
        Map<String, Object> expected = map(
            "feature_id", state.get("feature_id"),
            "stage", stage,
            "result", "approved",
            "attempt", approval.get("attempt"),
            "artifact_revision", approval.get("artifact_revision"),
            "artifact_sha256", approval.get("artifact_sha256"),
            "record_hash", approval.get("record_hash")
        );
        List<String> errors = new ArrayList<String>();
        for (Map.Entry<String, Object> entry : expected.entrySet()) {
            if (!Objects.equals(record.get(entry.getKey()), entry.getValue())) {
                errors.add(
                    "APPROVAL_CHAIN_BINDING_MISMATCH:" + stage + ":" + entry.getKey()
                );
            }
        }
        return errors;
    }

    static List<String> phaseReviewRecordBindingErrors(
        Path featureDir, Map<String, Object> state, String phase,
        Map<String, Object> review
    ) {
        Object approvalId = review.get("approval_id");
        if (approvalId != null) {
            return approvalRecordBindingErrors(
                featureDir, state, "phase-review:" + phase,
                map(
                    "approval_id", approvalId,
                    "attempt", review.get("attempt"),
                    "artifact_revision", review.get("tasks_revision"),
                    "artifact_sha256", review.get("tasks_sha256"),
                    "record_hash", review.get("record_hash")
                )
            );
        }
        for (Map<String, Object> event
            : readJsonl(featurePaths(featureDir).get("events"))) {
            Map<String, Object> payload = objectOrEmpty(event.get("payload"));
            if ("phase-approved".equals(text(event, "event_type"))
                && Objects.equals(event.get("attempt"), state.get("attempt"))
                && phase.equals(text(payload, "phase"))
                && Objects.equals(payload.get("source"), review.get("source"))
                && Objects.equals(
                    payload.get("approver_role"), review.get("approver_role")
                )) {
                return new ArrayList<String>();
            }
        }
        return listOf("PHASE_REVIEW_APPROVAL_CHAIN_MISSING:" + phase);
    }

    static List<String> approvalProjectionErrors(
        Path featureDir, Map<String, Object> state
    ) {
        List<String> errors = new ArrayList<String>();
        for (Map.Entry<String, Object> entry
            : objectOrEmpty(state.get("approvals")).entrySet()) {
            if (!(entry.getValue() instanceof Map<?, ?>)) {
                errors.add("APPROVAL_STATE_INVALID:" + entry.getKey());
                continue;
            }
            errors.addAll(approvalRecordBindingErrors(
                featureDir, state, entry.getKey(), object(entry.getValue())
            ));
        }
        for (Map.Entry<String, Object> entry
            : objectOrEmpty(state.get("phase_reviews")).entrySet()) {
            if (!(entry.getValue() instanceof Map<?, ?>)) {
                errors.add("PHASE_REVIEW_STATE_INVALID:" + entry.getKey());
                continue;
            }
            errors.addAll(phaseReviewRecordBindingErrors(
                featureDir, state, entry.getKey(), object(entry.getValue())
            ));
        }
        return errors;
    }

    static List<String> phaseReviewErrors(
        Path featureDir, Map<String, Object> state, String phase
    ) {
        Map<String, Object> review = objectOrEmpty(
            objectOrEmpty(state.get("phase_reviews")).get(phase)
        );
        if (!"approved".equals(text(review, "status"))) {
            return listOf("PHASE_REVIEW_NOT_APPROVED:" + phase);
        }
        List<String> errors = new ArrayList<String>(
            phaseReviewRecordBindingErrors(featureDir, state, phase, review)
        );
        Map<String, Object> tasks = objectOrEmpty(
            objectOrEmpty(state.get("artifacts")).get("tasks")
        );
        if (!Objects.equals(review.get("tasks_revision"), tasks.get("revision"))) {
            errors.add("PHASE_REVIEW_TASKS_REVISION_MISMATCH:" + phase);
        }
        if (!Objects.equals(review.get("tasks_sha256"), tasks.get("sha256"))) {
            errors.add("PHASE_REVIEW_TASKS_HASH_MISMATCH:" + phase);
        }
        return errors;
    }

    static List<String> approvalErrors(
        Path featureDir, Map<String, Object> state, String stage
    ) {
        Map<String, Object> approval = objectOrEmpty(
            objectOrEmpty(state.get("approvals")).get(stage)
        );
        Map<String, Object> artifact = objectOrEmpty(
            objectOrEmpty(state.get("artifacts")).get(stage)
        );
        if (!"approved".equals(text(approval, "status"))) {
            return listOf("APPROVAL_MISSING_OR_INVALID:" + stage);
        }
        if (artifact.isEmpty()) return listOf("APPROVED_ARTIFACT_MISSING:" + stage);
        List<String> errors = new ArrayList<String>();
        if (!Objects.equals(approval.get("attempt"), state.get("attempt"))) {
            errors.add("APPROVAL_ATTEMPT_MISMATCH:" + stage);
        }
        if (!Objects.equals(approval.get("artifact_sha256"), artifact.get("sha256"))) {
            errors.add("APPROVAL_HASH_MISMATCH:" + stage);
        }
        if (!Objects.equals(
            approval.get("artifact_revision"), artifact.get("revision")
        )) {
            errors.add("APPROVAL_REVISION_MISMATCH:" + stage);
        }
        if (!Objects.equals(
            currentArtifactHash(featureDir, stage), approval.get("artifact_sha256")
        )) {
            errors.add("APPROVAL_ARTIFACT_DRIFT:" + stage);
        }
        errors.addAll(
            approvalRecordBindingErrors(featureDir, state, stage, approval)
        );
        return errors;
    }

    static String stateTriple(String stage, String status, String action) {
        return stage + "\u0000" + status + "\u0000" + action;
    }

    static List<String> stateTransitionErrors(Map<String, Object> state) {
        String stage = text(state, "current_stage");
        String status = text(state, "stage_status");
        String action = text(state, "next_required_action");
        Object blocked = state.get("blocked");
        List<String> errors = new ArrayList<String>();
        if ("blocked".equals(status)) {
            Map<String, Object> block = objectOrEmpty(blocked);
            if (blank(text(block, "code"))) {
                return listOf("BLOCKED_STATE_REASON_MISSING");
            }
            Map<String, String> expectedByCode = linkedMap(
                PREMATURE_CHANGE_BLOCK,
                "restore-planning-baseline-before-current-gate",
                FEATURE_LAYOUT_BLOCK,
                "remove-unexpected-feature-paths-before-current-action",
                "IMPLEMENTATION_SCOPE_VIOLATION", "resolve-scope-violation",
                "CODE_REVIEW_BLOCKED", "resolve-code-review",
                "AUTO_FIX_FAILED", "resolve-auto-fix",
                "AUTO_FIX_BLOCKED", "resolve-auto-fix",
                "UNIT_TEST_FAILED", "resolve-unit-test",
                "UNIT_TEST_BLOCKED", "resolve-unit-test",
                "UNIT_TEST_NOT_RUN", "resolve-unit-test",
                "UNIT_TEST_SCOPE_CHANGED", "resolve-unit-test"
            );
            String expected = expectedByCode.get(text(block, "code"));
            if (expected == null) {
                errors.add("UNKNOWN_BLOCKED_STATE:" + text(block, "code"));
            } else if (!expected.equals(action)) {
                errors.add("BLOCKED_NEXT_ACTION_MISMATCH");
            }
            return errors;
        }
        if (TERMINAL_STATUSES.contains(status)) {
            Map<String, String> terminalActions = linkedMap(
                "completed", stateTriple("archive", "completed", "none"),
                "closed-with-risk", stateTriple("archive", "closed-with-risk", "none"),
                "aborted", stateTriple("archive", "aborted", "none"),
                "superseded", stateTriple("archive", "superseded", "none-historical-example")
            );
            if (!stateTriple(stage, status, action).equals(terminalActions.get(status))) {
                errors.add("TERMINAL_STATE_TRANSITION_MISMATCH");
            }
            return errors;
        }
        if (blocked != null) errors.add("BLOCK_REASON_PRESENT_OUTSIDE_BLOCKED_STATE");
        Set<String> valid = setOf(
            stateTriple("proposal-input", "ready", "assemble-proposal-input"),
            stateTriple("spec", "ready", "generate-spec"),
            stateTriple("spec", "awaiting-approval", "request-spec-approval"),
            stateTriple("design", "ready", "generate-design"),
            stateTriple("design", "awaiting-approval", "request-design-approval"),
            stateTriple("tasks", "ready", "generate-tasks"),
            stateTriple("tasks", "awaiting-approval", "request-tasks-approval"),
            stateTriple("implementation", "ready", "capture-implementation-scope"),
            stateTriple("code-review", "ready", "run-code-review"),
            stateTriple("code-review", "recorded", "record-code-review-gate"),
            stateTriple("auto-fix", "ready", "apply-review-findings"),
            stateTriple(
                "auto-fix", "ready",
                "record-auto-fix-not-required-or-current-fixes"
            ),
            stateTriple("auto-fix", "recorded", "record-auto-fix-gate"),
            stateTriple(
                "unit-test-summary", "ready", "generate-or-update-test-source"
            ),
            stateTriple(
                "unit-test-summary", "ready",
                "generate-unit-test-summary-from-evidence"
            ),
            stateTriple(
                "unit-test-summary", "recorded", "record-unit-test-gate"
            ),
            stateTriple(
                "unit-test-summary", "awaiting-approval",
                "request-unit-test-summary-approval"
            ),
            stateTriple("archive", "ready", "run-archive-check"),
            stateTriple("archive", "ready", "generate-archive-from-evidence"),
            stateTriple(
                "archive", "awaiting-final-approval", "request-archive-approval"
            )
        );
        if (valid.contains(stateTriple(stage, status, action))) {
            if ("generate-unit-test-summary-from-evidence".equals(action)
                && !(state.get("unit_test_execution") instanceof Map<?, ?>)) {
                errors.add("UNIT_TEST_EXECUTION_STATE_MISSING");
            }
            return errors;
        }
        if ("implementation".equals(stage) && "executing".equals(status)) {
            List<String> required = stringList(state.get("required_phases"));
            List<String> remaining = new ArrayList<String>();
            Map<String, Object> reviews = objectOrEmpty(state.get("phase_reviews"));
            for (String phase : required) {
                if (!"approved".equals(
                    text(objectOrEmpty(reviews.get(phase)), "status")
                )) remaining.add(phase);
            }
            if ("implement-next-approved-phase".equals(action)
                && remaining.size() == required.size()) return errors;
            if (!remaining.isEmpty()
                && ("implement-phase:" + remaining.get(0)).equals(action)) return errors;
            if (remaining.isEmpty()
                && "freeze-implementation-scope".equals(action)) return errors;
        }
        errors.add("INVALID_STATE_TRANSITION");
        return errors;
    }

    static List<String> workflowPrerequisiteErrors(
        Path featureDir, Map<String, Object> state, String ignoreArtifactStage
    ) {
        if ("historical-example".equals(text(state, "execution_mode"))) {
            return new ArrayList<String>();
        }
        String status = text(state, "stage_status");
        if (TERMINAL_STATUSES.contains(status) && !"completed".equals(status)) {
            return new ArrayList<String>();
        }
        String stage = text(state, "current_stage");
        if (!STAGE_ORDER.contains(stage)) return new ArrayList<String>();
        List<String> errors = new ArrayList<String>();
        Map<String, Object> artifacts = objectOrEmpty(state.get("artifacts"));
        List<String> requiredArtifacts = new ArrayList<String>();
        requiredArtifacts.add("brief-design");
        if (stageIndex(stage) >= stageIndex("spec")) requiredArtifacts.add("proposal-input");
        if (stageIndex(stage) >= stageIndex("design")) requiredArtifacts.add("spec");
        if (stageIndex(stage) >= stageIndex("tasks")) requiredArtifacts.add("design");
        if (stageIndex(stage) >= stageIndex("implementation")) requiredArtifacts.add("tasks");
        if (stageIndex(stage) >= stageIndex("auto-fix")) {
            requiredArtifacts.add("code-review-findings");
        }
        if (stageIndex(stage) >= stageIndex("unit-test-summary")) {
            requiredArtifacts.add("auto-fix-summary");
        }
        if (stageIndex(stage) >= stageIndex("archive")) {
            requiredArtifacts.add("unit-test-summary");
        }
        if ("spec".equals(stage) && "awaiting-approval".equals(status)) {
            requiredArtifacts.add("spec");
        }
        if ("design".equals(stage) && "awaiting-approval".equals(status)) {
            requiredArtifacts.add("design");
        }
        if ("tasks".equals(stage) && "awaiting-approval".equals(status)) {
            requiredArtifacts.add("tasks");
        }
        Map<String, Object> gates = objectOrEmpty(state.get("quality_gates"));
        if ("code-review".equals(stage)
            && ("recorded".equals(status)
                || artifacts.containsKey("code-review-findings")
                || gates.get("code-review") != null)) {
            requiredArtifacts.add("code-review-findings");
        }
        if ("auto-fix".equals(stage)
            && ("recorded".equals(status)
                || artifacts.containsKey("auto-fix-summary")
                || gates.get("auto-fix") != null)) {
            requiredArtifacts.add("auto-fix-summary");
        }
        if ("unit-test-summary".equals(stage)
            && (setOf("recorded", "awaiting-approval").contains(status)
                || gates.get("unit-test") != null)) {
            requiredArtifacts.add("unit-test-summary");
        }
        if ("archive".equals(stage)
            && setOf("awaiting-final-approval", "completed").contains(status)) {
            requiredArtifacts.add("archive");
        }
        for (String required : uniqueInOrder(requiredArtifacts)) {
            if (!artifacts.containsKey(required)) {
                errors.add("WORKFLOW_ARTIFACT_MISSING:" + required);
            }
        }

        List<String> requiredApprovals = new ArrayList<String>();
        if (stageIndex(stage) >= stageIndex("design")) requiredApprovals.add("spec");
        if (stageIndex(stage) >= stageIndex("tasks")) requiredApprovals.add("design");
        if (stageIndex(stage) >= stageIndex("implementation")) requiredApprovals.add("tasks");
        for (String required : requiredApprovals) {
            if (!required.equals(ignoreArtifactStage)) {
                errors.addAll(approvalErrors(featureDir, state, required));
            }
        }
        if (stageIndex(stage) >= stageIndex("code-review")) {
            for (String phase : stringList(state.get("required_phases"))) {
                errors.addAll(phaseReviewErrors(featureDir, state, phase));
            }
        }
        if (stageIndex(stage) >= stageIndex("auto-fix")) {
            Map<String, Object> review = objectOrEmpty(gates.get("code-review"));
            if (!setOf("passed", "failed").contains(text(review, "status"))) {
                errors.add("WORKFLOW_CODE_REVIEW_RESULT_MISSING");
            }
        }
        if (stageIndex(stage) >= stageIndex("unit-test-summary")) {
            Map<String, Object> review = objectOrEmpty(gates.get("code-review"));
            Map<String, Object> autoFix = objectOrEmpty(gates.get("auto-fix"));
            if (!"passed".equals(text(review, "status"))) {
                errors.add("WORKFLOW_CODE_REVIEW_NOT_PASSED");
            }
            if (!setOf("passed", "not-required").contains(text(autoFix, "status"))) {
                errors.add("WORKFLOW_AUTO_FIX_NOT_CLOSED");
            }
        }
        if (stageIndex(stage) >= stageIndex("archive")) {
            Map<String, Object> unit = objectOrEmpty(gates.get("unit-test"));
            if (!"passed".equals(text(unit, "status"))) {
                errors.add("WORKFLOW_UNIT_TEST_NOT_PASSED");
            }
            errors.addAll(approvalErrors(featureDir, state, "unit-test-summary"));
            if ("completed".equals(status)) {
                errors.addAll(approvalErrors(featureDir, state, "archive"));
            }
        }
        return errors;
    }

    static List<String> qualityGateEventErrors(
        Path featureDir, Map<String, Object> state
    ) {
        List<Map<String, Object>> events = readJsonl(
            featurePaths(featureDir).get("events")
        );
        List<String> errors = new ArrayList<String>();
        for (Map.Entry<String, Object> entry
            : objectOrEmpty(state.get("quality_gates")).entrySet()) {
            String gate = entry.getKey();
            if (!(entry.getValue() instanceof Map<?, ?>)) {
                errors.add("QUALITY_GATE_STATE_INVALID:" + gate);
                continue;
            }
            Map<String, Object> projection = object(entry.getValue());
            if (setOf("invalidated", "not-recorded").contains(
                text(projection, "status")
            )) continue;
            List<Map<String, Object>> matches = new ArrayList<Map<String, Object>>();
            for (Map<String, Object> event : events) {
                Map<String, Object> payload = objectOrEmpty(event.get("payload"));
                if ("quality-gate-recorded".equals(text(event, "event_type"))
                    && Objects.equals(event.get("attempt"), state.get("attempt"))
                    && gate.equals(text(payload, "gate"))) {
                    matches.add(event);
                }
            }
            if (matches.isEmpty()) {
                errors.add("QUALITY_GATE_EVENT_MISSING:" + gate);
                continue;
            }
            Map<String, Object> eventRecord = new LinkedHashMap<String, Object>(
                objectOrEmpty(matches.get(matches.size() - 1).get("payload"))
            );
            eventRecord.remove("gate");
            if (!eventRecord.equals(projection)) {
                errors.add("QUALITY_GATE_EVENT_BINDING_MISMATCH:" + gate);
            }
        }
        return errors;
    }

    static Map<String, Object> scopeContractPayload(Map<String, Object> scope) {
        List<String> fields = listOf(
            "feature_id", "attempt", "repository_id", "feature_repo_path",
            "branch", "base_commit", "allowed_paths", "forbidden_paths",
            "required_phases", "production_change", "test_path_patterns"
        );
        for (String field : fields) {
            if (!scope.containsKey(field)) throw new ControlError("SCOPE_MANIFEST_INVALID");
        }
        LinkedHashMap<String, Object> result = new LinkedHashMap<String, Object>();
        for (String field : fields) result.put(field, scope.get(field));
        return result;
    }

    static Map<String, Object> issueImplementationPermit(
        Path featureDir, Map<String, Object> state, Map<String, Object> scope
    ) {
        Map<String, Object> approvedArtifacts = new LinkedHashMap<String, Object>();
        List<String> errors = new ArrayList<String>();
        Map<String, Object> artifacts = objectOrEmpty(state.get("artifacts"));
        Map<String, Object> approvals = objectOrEmpty(state.get("approvals"));
        for (String stage : listOf("spec", "design", "tasks")) {
            errors.addAll(approvalErrors(featureDir, state, stage));
            Map<String, Object> artifact = objectOrEmpty(artifacts.get(stage));
            Map<String, Object> approval = objectOrEmpty(approvals.get(stage));
            if (!artifact.isEmpty() && !approval.isEmpty()) {
                approvedArtifacts.put(stage, map(
                    "revision", artifact.get("revision"),
                    "sha256", artifact.get("sha256"),
                    "approval_id", approval.get("approval_id")
                ));
            }
        }
        if (!errors.isEmpty()) {
            throw new ControlError(
                "IMPLEMENTATION_PERMIT_REJECTED:"
                + String.join(",", sortedUnique(errors))
            );
        }
        String scopeHash = sha256Bytes(
            canonicalJson(scopeContractPayload(scope)).getBytes(StandardCharsets.UTF_8)
        );
        Map<String, Object> permit = map(
            "status", "active",
            "feature_id", state.get("feature_id"),
            "attempt", state.get("attempt"),
            "issued_at", utcNow(),
            "approved_artifacts", approvedArtifacts,
            "scope_contract_sha256", scopeHash
        );
        permit.put(
            "permit_sha256",
            sha256Bytes(canonicalJson(permit).getBytes(StandardCharsets.UTF_8))
        );
        scope.put("scope_contract_sha256", scopeHash);
        scope.put("implementation_permit_sha256", permit.get("permit_sha256"));
        return permit;
    }

    static List<String> implementationPermitErrors(
        Path featureDir, Map<String, Object> state, Map<String, Object> providedScope
    ) {
        if (!(state.get("implementation_permit") instanceof Map<?, ?>)) {
            return listOf("IMPLEMENTATION_PERMIT_MISSING_OR_INACTIVE");
        }
        Map<String, Object> permit = object(state.get("implementation_permit"));
        if (!"active".equals(text(permit, "status"))) {
            return listOf("IMPLEMENTATION_PERMIT_MISSING_OR_INACTIVE");
        }
        List<String> errors = new ArrayList<String>();
        if (!Objects.equals(permit.get("feature_id"), state.get("feature_id"))) {
            errors.add("IMPLEMENTATION_PERMIT_FEATURE_MISMATCH");
        }
        if (!Objects.equals(permit.get("attempt"), state.get("attempt"))) {
            errors.add("IMPLEMENTATION_PERMIT_ATTEMPT_MISMATCH");
        }
        Map<String, Object> body = new LinkedHashMap<String, Object>(permit);
        Object actualPermitHash = body.remove("permit_sha256");
        String expectedPermitHash = sha256Bytes(
            canonicalJson(body).getBytes(StandardCharsets.UTF_8)
        );
        if (!Objects.equals(actualPermitHash, expectedPermitHash)) {
            errors.add("IMPLEMENTATION_PERMIT_HASH_MISMATCH");
        }
        Map<String, Object> artifacts = objectOrEmpty(state.get("artifacts"));
        Map<String, Object> approvals = objectOrEmpty(state.get("approvals"));
        Map<String, Object> bindings = objectOrEmpty(permit.get("approved_artifacts"));
        for (String stage : listOf("spec", "design", "tasks")) {
            errors.addAll(approvalErrors(featureDir, state, stage));
            Map<String, Object> artifact = objectOrEmpty(artifacts.get(stage));
            Map<String, Object> approval = objectOrEmpty(approvals.get(stage));
            Map<String, Object> binding = objectOrEmpty(bindings.get(stage));
            if (!Objects.equals(binding.get("revision"), artifact.get("revision"))) {
                errors.add(
                    "IMPLEMENTATION_PERMIT_ARTIFACT_REVISION_MISMATCH:" + stage
                );
            }
            if (!Objects.equals(binding.get("sha256"), artifact.get("sha256"))) {
                errors.add("IMPLEMENTATION_PERMIT_ARTIFACT_HASH_MISMATCH:" + stage);
            }
            if (!Objects.equals(
                binding.get("approval_id"), approval.get("approval_id")
            )) {
                errors.add("IMPLEMENTATION_PERMIT_APPROVAL_MISMATCH:" + stage);
            }
        }
        Map<String, Object> scope = providedScope;
        if (scope == null) {
            Path scopePath = featurePaths(featureDir).get("scope");
            if (!Files.isRegularFile(scopePath)) {
                errors.add("IMPLEMENTATION_PERMIT_SCOPE_MISSING");
                return sortedUnique(errors);
            }
            try {
                scope = loadScope(featureDir);
            } catch (ControlError exc) {
                errors.add("SCOPE_MANIFEST_INVALID");
                return sortedUnique(errors);
            }
        }
        String expectedScopeHash;
        try {
            expectedScopeHash = sha256Bytes(
                canonicalJson(scopeContractPayload(scope))
                    .getBytes(StandardCharsets.UTF_8)
            );
        } catch (ControlError exc) {
            errors.add("SCOPE_MANIFEST_INVALID");
            return sortedUnique(errors);
        }
        if (!Objects.equals(scope.get("scope_contract_sha256"), expectedScopeHash)) {
            errors.add("IMPLEMENTATION_PERMIT_SCOPE_CONTRACT_HASH_MISMATCH");
        }
        if (!Objects.equals(
            permit.get("scope_contract_sha256"), expectedScopeHash
        )) {
            errors.add("IMPLEMENTATION_PERMIT_SCOPE_BINDING_MISMATCH");
        }
        if (!Objects.equals(
            scope.get("implementation_permit_sha256"), actualPermitHash
        )) {
            errors.add("IMPLEMENTATION_PERMIT_SCOPE_PERMIT_MISMATCH");
        }
        return sortedUnique(errors);
    }

    static void assertImplementationPermit(
        Path featureDir, Map<String, Object> state, Map<String, Object> scope
    ) {
        List<String> errors = implementationPermitErrors(featureDir, state, scope);
        if (!errors.isEmpty()) {
            throw new ControlError(
                "IMPLEMENTATION_PERMIT_INVALID:" + String.join(",", errors)
            );
        }
    }

    static boolean revokeImplementationPermit(
        Path featureDir, Map<String, Object> state, String reason
    ) {
        if (!(state.get("implementation_permit") instanceof Map<?, ?>)) return false;
        Map<String, Object> historical = new LinkedHashMap<String, Object>(
            object(state.get("implementation_permit"))
        );
        historical.put("status", "invalidated");
        historical.put("invalidated_at", utcNow());
        historical.put("invalidated_reason", reason);
        arrayOrEmptyPut(state, "implementation_permit_history", historical);
        state.put("implementation_permit", null);
        state.put("required_phases", new ArrayList<Object>());
        state.put("unit_test_execution", null);
        try {
            Files.deleteIfExists(featurePaths(featureDir).get("scope"));
            Files.deleteIfExists(featurePaths(featureDir).get("unit_test_evidence"));
            Files.deleteIfExists(featurePaths(featureDir).get("archive_evidence"));
        } catch (IOException exc) {
            throw new ControlError("Cannot revoke implementation permit files", exc);
        }
        return true;
    }

    static List<String> qualityGateErrors(
        Path featureDir, Map<String, Object> state
    ) {
        Map<String, Object> scope;
        Map<String, Object> current;
        try {
            scope = loadScope(featureDir);
            current = snapshotForScope(scopeRepoRoot(featureDir, scope), scope);
        } catch (RuntimeException exc) {
            return listOf("SCOPE_MANIFEST_INVALID");
        }
        List<String> violations = stringList(current.get("violations"));
        if (!violations.isEmpty()) return violations;
        String currentHash = text(current, "snapshot_sha256");
        Map<String, Set<String>> accepted = new LinkedHashMap<String, Set<String>>();
        accepted.put("code-review", setOf("passed"));
        accepted.put("auto-fix", setOf("passed", "not-required"));
        accepted.put("unit-test", setOf("passed"));
        List<String> errors = new ArrayList<String>();
        Map<String, Object> gates = objectOrEmpty(state.get("quality_gates"));
        Map<String, Object> artifacts = objectOrEmpty(state.get("artifacts"));
        for (Map.Entry<String, Set<String>> entry : accepted.entrySet()) {
            String gate = entry.getKey();
            Map<String, Object> record = objectOrEmpty(gates.get(gate));
            if (!entry.getValue().contains(text(record, "status"))) {
                errors.add("QUALITY_GATE_NOT_PASSED:" + gate);
                continue;
            }
            if (!Objects.equals(record.get("scope_sha256"), currentHash)) {
                errors.add("QUALITY_GATE_SCOPE_MISMATCH:" + gate);
            }
            String artifactStage;
            if ("code-review".equals(gate)) artifactStage = "code-review-findings";
            else if ("auto-fix".equals(gate)) artifactStage = "auto-fix-summary";
            else artifactStage = "unit-test-summary";
            Map<String, Object> artifact = objectOrEmpty(artifacts.get(artifactStage));
            if (artifact.isEmpty()
                || !Objects.equals(
                    record.get("artifact_sha256"), artifact.get("sha256")
                )) {
                errors.add("QUALITY_GATE_ARTIFACT_MISMATCH:" + gate);
            } else if (!Objects.equals(artifact.get("scope_sha256"), currentHash)) {
                errors.add("QUALITY_GATE_ARTIFACT_SCOPE_MISMATCH:" + gate);
            }
            if ("unit-test".equals(gate)
                && "passed".equals(text(record, "status"))) {
                errors.addAll(
                    unitTestExecutionErrors(featureDir, state, "passed")
                );
                Map<String, Object> execution = objectOrEmpty(
                    state.get("unit_test_execution")
                );
                if (!Objects.equals(
                    record.get("test_execution_sha256"),
                    execution.get("evidence_sha256")
                )) {
                    errors.add("QUALITY_GATE_TEST_EXECUTION_MISMATCH:unit-test");
                }
            }
        }
        return errors;
    }

    static List<String> archiveEvidenceErrors(
        Path featureDir, Map<String, Object> state
    ) {
        Path path = featurePaths(featureDir).get("archive_evidence");
        if (!Files.isRegularFile(path)) return listOf("ARCHIVE_EVIDENCE_MISSING");
        Map<String, Object> evidence;
        Map<String, Object> scope;
        try {
            evidence = readJson(path);
        } catch (ControlError exc) {
            return listOf("ARCHIVE_EVIDENCE_INVALID");
        }
        try {
            scope = loadScope(featureDir);
        } catch (ControlError exc) {
            return listOf("SCOPE_MANIFEST_INVALID");
        }
        Map<String, Object> frozen = objectOrEmpty(scope.get("frozen_snapshot"));
        Map<String, Object> unitGate = objectOrEmpty(
            objectOrEmpty(state.get("quality_gates")).get("unit-test")
        );
        Map<String, Object> expected = map(
            "feature_id", state.get("feature_id"),
            "attempt", state.get("attempt"),
            "base_commit", scope.get("base_commit"),
            "head_commit", frozen.get("head_commit"),
            "head_tree", frozen.get("head_tree"),
            "scope_sha256", frozen.get("snapshot_sha256"),
            "unit_test_evidence_sha256", unitGate.get("test_execution_sha256")
        );
        List<String> errors = new ArrayList<String>();
        for (Map.Entry<String, Object> entry : expected.entrySet()) {
            if (!Objects.equals(evidence.get(entry.getKey()), entry.getValue())) {
                errors.add("ARCHIVE_EVIDENCE_MISMATCH:" + entry.getKey());
            }
        }
        if (!Objects.equals(evidence.get("files"), frozen.get("files"))) {
            errors.add("ARCHIVE_EVIDENCE_MISMATCH:files");
        }
        Map<String, Object> body = new LinkedHashMap<String, Object>(evidence);
        body.remove("evidence_sha256");
        String hash = sha256Bytes(
            canonicalJson(body).getBytes(StandardCharsets.UTF_8)
        );
        if (!Objects.equals(evidence.get("evidence_sha256"), hash)) {
            errors.add("ARCHIVE_EVIDENCE_HASH_MISMATCH");
        }
        return errors;
    }

    static List<String> archiveErrors(
        Path featureDir, Map<String, Object> state, boolean requireArchive
    ) {
        List<String> errors = new ArrayList<String>();
        Map<String, Path> paths = featurePaths(featureDir);
        errors.addAll(verifyLock(featureDir, state));
        errors.addAll(validateHashChain(paths.get("events"), "event_hash"));
        errors.addAll(validateHashChain(paths.get("approvals"), "record_hash"));
        errors.addAll(stateEventProjectionErrors(featureDir, state));
        errors.addAll(stateTransitionErrors(state));
        errors.addAll(approvalProjectionErrors(featureDir, state));
        errors.addAll(workflowPrerequisiteErrors(featureDir, state, null));
        errors.addAll(qualityGateEventErrors(featureDir, state));
        List<String> generationErrors = featureGenerationErrors(
            featureDir, state, null
        );
        errors.addAll(generationErrors);
        if (!generationErrors.isEmpty()) return sortedUnique(errors);
        errors.addAll(artifactDrift(featureDir, state));
        for (String stage : listOf("spec", "design", "tasks", "unit-test-summary")) {
            errors.addAll(approvalErrors(featureDir, state, stage));
        }
        for (String phase : stringList(state.get("required_phases"))) {
            errors.addAll(phaseReviewErrors(featureDir, state, phase));
        }
        if (!Files.exists(paths.get("scope"))) {
            errors.add("SCOPE_MANIFEST_MISSING");
        } else {
            errors.addAll(qualityGateErrors(featureDir, state));
            errors.addAll(archiveEvidenceErrors(featureDir, state));
        }
        List<String> required = new ArrayList<String>(ARTIFACT_FILES.keySet());
        if (!requireArchive) required.remove("archive");
        Map<String, Object> artifacts = objectOrEmpty(state.get("artifacts"));
        for (String stage : required) {
            if (!artifacts.containsKey(stage)) {
                errors.add("ARTIFACT_NOT_RECORDED:" + stage);
            }
        }
        if (state.get("blocked") != null) errors.add("FEATURE_BLOCKED");
        return sortedUnique(errors);
    }

    static Map<String, Object> validateState(
        Path featureDir, Map<String, Object> state
    ) {
        List<String> errors = new ArrayList<String>();
        List<String> warnings = new ArrayList<String>();
        Set<String> required = setOf(
            "schema_version", "feature_id", "feature_dir", "execution_mode",
            "entry_contract", "revision", "attempt", "current_stage",
            "stage_status", "artifacts", "approvals", "quality_gates",
            "phase_reviews", "planning_baseline", "implementation_started",
            "implementation_permit", "next_required_action"
        );
        for (String field : new TreeSet<String>(required)) {
            if (!state.containsKey(field)) errors.add("STATE_FIELD_MISSING:" + field);
        }
        Map<String, Object> entryContract = objectOrEmpty(state.get("entry_contract"));
        if (!"brief-prompt-and-skill-call".equals(
            text(entryContract, "user_entry")
        )) {
            errors.add("USER_ENTRY_CONTRACT_CHANGED");
        }
        if (!Boolean.FALSE.equals(entryContract.get("developer_action_required"))) {
            errors.add("USER_ENTRY_REQUIRES_NEW_ACTION");
        }
        if (!STAGE_ORDER.contains(text(state, "current_stage"))) {
            errors.add("INVALID_CURRENT_STAGE");
        }
        Map<String, Path> paths = featurePaths(featureDir);
        errors.addAll(stateTransitionErrors(state));
        errors.addAll(verifyLock(featureDir, state));
        errors.addAll(artifactDrift(featureDir, state));
        errors.addAll(validateHashChain(paths.get("events"), "event_hash"));
        errors.addAll(validateHashChain(paths.get("approvals"), "record_hash"));
        errors.addAll(stateEventProjectionErrors(featureDir, state));
        errors.addAll(approvalProjectionErrors(featureDir, state));
        errors.addAll(workflowPrerequisiteErrors(featureDir, state, null));
        errors.addAll(qualityGateEventErrors(featureDir, state));
        List<Map<String, Object>> events = readJsonl(paths.get("events"));
        if (!events.isEmpty()
            && events.get(events.size() - 1).get("state_sha256") == null) {
            warnings.add("LEGACY_STATE_EVENT_WITHOUT_PROJECTION_HASH");
        }
        if (!"historical-example".equals(text(state, "execution_mode"))) {
            List<String> generationErrors = featureGenerationErrors(
                featureDir, state, null
            );
            errors.addAll(generationErrors);
            if (generationErrors.isEmpty()) {
                if (state.get("unit_test_execution") != null) {
                    errors.addAll(unitTestExecutionErrors(featureDir, state, null));
                }
                errors.addAll(planningGuardErrors(featureDir, state));
                errors.addAll(scopeDrift(featureDir, state));
                if (state.get("implementation_permit") != null
                    || Files.exists(paths.get("scope"))) {
                    errors.addAll(
                        implementationPermitErrors(featureDir, state, null)
                    );
                }
            }
        } else {
            warnings.add("HISTORICAL_EXAMPLE_NOT_VALID_GATE_EVIDENCE");
        }
        return map(
            "errors", sortedUnique(errors),
            "warnings", sortedUnique(warnings)
        );
    }

    static void assertControlIntegrity(
        Path featureDir, Map<String, Object> state,
        String ignoreArtifactStage, boolean allowScopeDrift
    ) {
        List<String> errors = new ArrayList<String>();
        Map<String, Path> paths = featurePaths(featureDir);
        errors.addAll(verifyLock(featureDir, state));
        errors.addAll(validateHashChain(paths.get("events"), "event_hash"));
        errors.addAll(validateHashChain(paths.get("approvals"), "record_hash"));
        errors.addAll(stateEventProjectionErrors(featureDir, state));
        errors.addAll(stateTransitionErrors(state));
        errors.addAll(approvalProjectionErrors(featureDir, state));
        errors.addAll(workflowPrerequisiteErrors(
            featureDir, state, ignoreArtifactStage
        ));
        errors.addAll(qualityGateEventErrors(featureDir, state));
        for (String error : artifactDrift(featureDir, state)) {
            if (ignoreArtifactStage != null
                && (error.startsWith("ARTIFACT_DRIFT:" + ignoreArtifactStage + ":")
                    || error.startsWith(
                        "ARTIFACT_MISSING:" + ignoreArtifactStage + ":"
                    ))) continue;
            errors.add(error);
        }
        List<String> generationErrors = featureGenerationErrors(
            featureDir, state, ignoreArtifactStage
        );
        if (!generationErrors.isEmpty()) {
            if (errors.isEmpty()
                && !TERMINAL_STATUSES.contains(text(state, "stage_status"))) {
                blockUnexpectedFeatureLayout(featureDir, state, generationErrors);
            }
            errors.addAll(generationErrors);
        } else {
            List<String> premature = planningGuardErrors(featureDir, state);
            if (!premature.isEmpty()) {
                blockPrematureImplementationChange(featureDir, state, premature);
                errors.addAll(premature);
            }
        }
        if (generationErrors.isEmpty()
            && (state.get("implementation_permit") != null
                || Files.exists(paths.get("scope")))
            && !setOf(
                "brief-design", "proposal-input", "spec", "design", "tasks"
            ).contains(ignoreArtifactStage)) {
            errors.addAll(implementationPermitErrors(featureDir, state, null));
        }
        if (generationErrors.isEmpty()
            && state.get("unit_test_execution") != null) {
            errors.addAll(unitTestExecutionErrors(featureDir, state, null));
        }
        if (generationErrors.isEmpty() && !allowScopeDrift
            && !"historical-example".equals(text(state, "execution_mode"))) {
            errors.addAll(scopeDrift(featureDir, state));
        }
        if (!errors.isEmpty()) {
            throw new ControlError(
                "Control integrity check failed: "
                + String.join(", ", sortedUnique(errors))
            );
        }
    }

    static void assertHistoryAndLock(
        Path featureDir, Map<String, Object> state
    ) {
        List<String> errors = new ArrayList<String>();
        Map<String, Path> paths = featurePaths(featureDir);
        errors.addAll(verifyLock(featureDir, state));
        errors.addAll(validateHashChain(paths.get("events"), "event_hash"));
        errors.addAll(validateHashChain(paths.get("approvals"), "record_hash"));
        errors.addAll(stateEventProjectionErrors(featureDir, state));
        errors.addAll(stateTransitionErrors(state));
        errors.addAll(approvalProjectionErrors(featureDir, state));
        errors.addAll(workflowPrerequisiteErrors(featureDir, state, null));
        errors.addAll(qualityGateEventErrors(featureDir, state));
        if (!errors.isEmpty()) {
            throw new ControlError(
                "Control history check failed: "
                + String.join(", ", sortedUnique(errors))
            );
        }
    }

    static void assertArtifactEntry(
        Path featureDir, Map<String, Object> state, String stage,
        Map<String, Object> previous
    ) {
        Set<String> revisablePlanning = setOf(
            "brief-design", "proposal-input", "spec", "design", "tasks"
        );
        if (previous != null && revisablePlanning.contains(stage)) return;
        Map<String, String> expectedStages = linkedMap(
            "proposal-input", "proposal-input",
            "spec", "spec",
            "design", "design",
            "tasks", "tasks",
            "code-review-findings", "code-review",
            "auto-fix-summary", "auto-fix",
            "unit-test-summary", "unit-test-summary",
            "archive", "archive"
        );
        String expectedStage = expectedStages.get(stage);
        if (expectedStage != null
            && !expectedStage.equals(text(state, "current_stage"))) {
            throw new ControlError(
                "Cannot record " + stage + " while current_stage="
                + text(state, "current_stage") + "; expected " + expectedStage
            );
        }
        Map<String, Object> artifacts = objectOrEmpty(state.get("artifacts"));
        if ("proposal-input".equals(stage)
            && !artifacts.containsKey("brief-design")) {
            throw new ControlError("proposal-input requires recorded brief-design");
        }
        if ("spec".equals(stage) && !artifacts.containsKey("proposal-input")) {
            throw new ControlError("spec requires recorded proposal-input");
        }
        if ("design".equals(stage)) {
            List<String> errors = approvalErrors(featureDir, state, "spec");
            if (!errors.isEmpty()) {
                throw new ControlError(
                    "design requires current Spec approval: "
                    + String.join(", ", errors)
                );
            }
        }
        if ("tasks".equals(stage)) {
            List<String> errors = approvalErrors(featureDir, state, "design");
            if (!errors.isEmpty()) {
                throw new ControlError(
                    "tasks requires current Design approval: "
                    + String.join(", ", errors)
                );
            }
        }
        if ("code-review-findings".equals(stage)) {
            List<String> errors = new ArrayList<String>(
                approvalErrors(featureDir, state, "tasks")
            );
            for (String phase : stringList(state.get("required_phases"))) {
                errors.addAll(phaseReviewErrors(featureDir, state, phase));
            }
            requireCurrentScope(featureDir, state);
            if (!errors.isEmpty()) {
                throw new ControlError(
                    "Code Review findings entry blocked: "
                    + String.join(", ", errors)
                );
            }
        }
        if ("auto-fix-summary".equals(stage)) {
            Map<String, Object> review = objectOrEmpty(
                objectOrEmpty(state.get("quality_gates")).get("code-review")
            );
            if (!setOf("passed", "failed").contains(text(review, "status"))) {
                throw new ControlError(
                    "Auto-fix summary requires a completed Code Review result"
                );
            }
        }
        if ("unit-test-summary".equals(stage)) {
            List<String> errors = qualityGateErrors(featureDir, state).stream()
                .filter(value -> !"QUALITY_GATE_NOT_PASSED:unit-test".equals(value))
                .collect(Collectors.toList());
            if (!errors.isEmpty()) {
                throw new ControlError(
                    "Unit Test Summary entry blocked: "
                    + String.join(", ", errors)
                );
            }
            if (state.get("unit_test_execution") instanceof Map<?, ?>) {
                errors = unitTestExecutionErrors(featureDir, state, null);
                if (!errors.isEmpty()) {
                    throw new ControlError(
                        "Unit Test Summary execution evidence is invalid: "
                        + String.join(", ", errors)
                    );
                }
                String content;
                try {
                    content = readUtf8(featureDir.resolve(ARTIFACT_FILES.get(stage)));
                } catch (IOException exc) {
                    throw new ControlError(
                        "Cannot read Unit Test Summary before recording", exc
                    );
                }
                Map<String, Object> execution = object(state.get("unit_test_execution"));
                for (String field : listOf("evidence_sha256", "scope_sha256")) {
                    String expected = text(execution, field);
                    if (expected == null || !content.contains(expected)) {
                        throw new ControlError(
                            "Unit Test Summary must include current " + field
                        );
                    }
                }
            }
        }
        if ("archive".equals(stage)) {
            List<String> errors = archiveEvidenceErrors(featureDir, state);
            if (!errors.isEmpty()) {
                throw new ControlError(
                    "Archive entry blocked: " + String.join(", ", errors)
                );
            }
        }
    }

    // Command handlers.

    static void ensureRuntimeIntegrity() {
        if (verifiedRuntimeSha256 != null) return;
        Path runtime;
        try {
            if (Sdd2Control.class.getProtectionDomain().getCodeSource() == null) {
                throw new ControlError(
                    "CONTROLLER_PACKAGE_INVALID:无法定位 SDD2.0 控制器 JAR。"
                );
            }
            runtime = Paths.get(
                Sdd2Control.class.getProtectionDomain()
                    .getCodeSource().getLocation().toURI()
            ).toAbsolutePath().normalize();
        } catch (ControlError exc) {
            throw exc;
        } catch (Exception exc) {
            throw new ControlError(
                "CONTROLLER_PACKAGE_INVALID:无法定位 SDD2.0 控制器 JAR。"
                    + "请重新获取完整运行包。",
                exc
            );
        }
        if (!Files.isRegularFile(runtime)
            || !runtime.getFileName().toString().endsWith(".jar")) {
            throw new ControlError(
                "CONTROLLER_PACKAGE_INVALID:正式流程必须运行预编译的 "
                    + "sdd2-control.jar，不得现场运行源码或 class 文件。"
            );
        }
        Path checksum = runtime.resolveSibling(RUNTIME_CHECKSUM_FILE);
        if (!Files.isRegularFile(checksum)) {
            throw new ControlError(
                "CONTROLLER_INTEGRITY_FILE_MISSING:缺少 "
                    + RUNTIME_CHECKSUM_FILE + "。请重新获取完整的 SDD2.0 "
                    + "Java 8 控制器运行包。"
            );
        }
        String expected;
        try {
            String content = readUtf8(checksum).trim();
            expected = content.split("\\s+", 2)[0].toLowerCase(Locale.ROOT);
        } catch (IOException exc) {
            throw new ControlError(
                "CONTROLLER_INTEGRITY_FILE_INVALID:无法读取控制器完整性文件。"
                    + "请重新获取完整运行包。",
                exc
            );
        }
        if (!expected.matches("[0-9a-f]{64}")) {
            throw new ControlError(
                "CONTROLLER_INTEGRITY_FILE_INVALID:控制器完整性文件格式错误。"
                    + "请重新获取完整运行包。"
            );
        }
        String actual = sha256File(runtime);
        if (!expected.equals(actual)) {
            throw new ControlError(
                "CONTROLLER_INTEGRITY_MISMATCH:控制器 JAR 已损坏或与校验文件"
                    + "不匹配。请重新获取完整的 sdd2-control.jar 和 "
                    + RUNTIME_CHECKSUM_FILE + "。"
            );
        }
        verifiedRuntimeSha256 = actual;
    }

    static Map<String, Object> cmdDoctor(Opts args) {
        String specification = System.getProperty("java.specification.version", "");
        int major;
        try {
            major = specification.startsWith("1.")
                ? Integer.parseInt(specification.substring(2))
                : Integer.parseInt(specification.split("\\.", 2)[0]);
        } catch (RuntimeException exc) {
            throw new ControlError(
                "JAVA_RUNTIME_INVALID:无法识别当前 Java 版本。请安装或启用 Java 8 及以上版本，"
                + "并正确配置 PATH/JAVA_HOME。"
            );
        }
        if (major < 8) {
            throw new ControlError(
                "JAVA_RUNTIME_TOO_OLD:当前 Java 版本低于 Java 8。请安装或启用 Java 8 及以上版本，"
                + "并正确配置 PATH/JAVA_HOME。"
            );
        }
        Path repoRoot = Paths.get(args.one("--repo-root", "."))
            .toAbsolutePath().normalize();
        if (!Files.isDirectory(repoRoot)) {
            throw new ControlError("RUNTIME_REPOSITORY_NOT_FOUND:仓库目录不存在：" + repoRoot);
        }
        ProcResult git;
        try {
            git = runProcess(listOf("git", "--version"), repoRoot, 30, null);
        } catch (ControlError exc) {
            throw new ControlError(
                "GIT_RUNTIME_MISSING:未检测到可用 Git。请安装或启用 Git，并确认 git 已加入 PATH。"
            );
        }
        if (git.exitCode != 0) {
            throw new ControlError(
                "GIT_RUNTIME_INVALID:Git 无法正常启动。请检查 Git 安装及 PATH 配置。"
            );
        }
        return map(
            "runtime", "java",
            "java_specification_version", specification,
            "java_8_compatible", true,
            "git_version", git.stdout.trim(),
            "schema_version", SCHEMA_VERSION,
            "controller_version", "2.0-java8.2",
            "jar_sha256", verifiedRuntimeSha256,
            "jar_integrity_verified", true,
            "wrote_feature_files", false,
            "message", "SDD2.0 Java 8 控制器运行环境检查通过"
        );
    }

    static Map<String, Object> cmdInit(Opts args) {
        String featureId = args.required("--feature-id");
        String mode = args.one("--mode", "real");
        if (!setOf("real", "demo").contains(mode)) {
            throw new ControlError("Invalid --mode: " + mode + "; expected real or demo");
        }
        Path featureDir = normalizeFeatureDir(args.required("--feature-dir"));
        Map<String, Path> paths = featurePaths(featureDir);
        if (Files.exists(paths.get("state"))) {
            throw new ControlError(
                "Feature is already initialized: " + paths.get("state")
            );
        }
        Path repoRoot = gitRoot(featureDir);
        List<String> boundaryErrors = new ArrayList<String>(
            featureLocationErrors(repoRoot, featureDir)
        );
        if (!boundaryErrors.isEmpty()) {
            throw new ControlError(
                "FEATURE_GENERATION_BOUNDARY_REJECTED:"
                + String.join(",", boundaryErrors)
            );
        }
        recoverIncompleteInitialization(repoRoot, featureDir, featureId);
        String featureRepoPath = relative(repoRoot, featureDir);
        boundaryErrors.addAll(featureLayoutErrors(featureDir, null, null));
        boundaryErrors.addAll(
            uncontrolledSiblingFeatureErrors(repoRoot, featureRepoPath)
        );
        if (!boundaryErrors.isEmpty()) {
            throw new ControlError(
                "FEATURE_GENERATION_BOUNDARY_REJECTED:"
                + String.join(",", sortedUnique(boundaryErrors))
            );
        }
        Path brief = featureDir.resolve(ARTIFACT_FILES.get("brief-design"));
        if (!Files.isRegularFile(brief)) {
            throw new ControlError(
                "brief-design.md must be persisted before SDD2 initialization"
            );
        }
        validateArtifactLanguage(brief, "brief-design");
        String branch = runGit(repoRoot, "branch", "--show-current");
        if (branch.isEmpty()) {
            throw new ControlError(
                "Detached HEAD is not allowed for an active SDD2 feature"
            );
        }
        List<String> installedGuards = installGitGuards(repoRoot);
        boolean lockAcquired = acquireLock(repoRoot, featureDir, featureId);
        if (!lockAcquired) {
            throw new ControlError("Incomplete initialization has unrecognized evidence; preserve it for recovery");
        }
        try {
            String briefDigest = sha256File(brief);
            String briefSnapshot = persistArtifactSnapshot(
                featureDir, "brief-design", 1, briefDigest
            );
            Map<String, Object> baseline = planningSnapshot(
                repoRoot, featureRepoPath
            );
            Map<String, Object> artifacts = map(
                "brief-design", map(
                    "path", ARTIFACT_FILES.get("brief-design"),
                    "revision", 1L,
                    "sha256", briefDigest,
                    "snapshot_path", briefSnapshot,
                    "status", "recorded",
                    "recorded_at", utcNow()
                )
            );
            Map<String, Object> state = map(
                "schema_version", SCHEMA_VERSION,
                "feature_id", featureId,
                "feature_dir", featureRepoPath,
                "feature_repo_path", featureRepoPath,
                "execution_mode", mode,
                "entry_contract", map(
                    "user_entry", "brief-prompt-and-skill-call",
                    "developer_action_required", false,
                    "version", 1L
                ),
                "workspace_binding", map(
                    "repo_root", ".",
                    "worktree", ".",
                    "repository_id", repositoryId(repoRoot),
                    "branch", branch
                ),
                "revision", 1L,
                "attempt", 1L,
                "current_stage", "proposal-input",
                "stage_status", "ready",
                "last_completed_stage", "brief-design",
                "next_required_action", "assemble-proposal-input",
                "blocked", null,
                "artifacts", artifacts,
                "approvals", new LinkedHashMap<String, Object>(),
                "quality_gates", new LinkedHashMap<String, Object>(),
                "required_phases", new ArrayList<Object>(),
                "phase_reviews", new LinkedHashMap<String, Object>(),
                "invalidations", new ArrayList<Object>(),
                "demo_authorization", null,
                "planning_baseline", baseline,
                "implementation_started", false,
                "implementation_permit", null,
                "implementation_permit_history", new ArrayList<Object>(),
                "unit_test_execution", null,
                "created_at", utcNow(),
                "updated_at", utcNow()
            );
            try {
                Files.createDirectories(paths.get("control"));
                if (!Files.exists(paths.get("approvals"))) {
                    Files.createFile(paths.get("approvals"));
                }
                if (!Files.exists(paths.get("events"))) {
                    Files.createFile(paths.get("events"));
                }
            } catch (IOException exc) {
                throw new ControlError("Cannot initialize Feature control files", exc);
            }
            saveState(featureDir, state);
            appendEvent(
                featureDir, state, "feature-initialized",
                map(
                    "mode", state.get("execution_mode"),
                    "planning_baseline_sha256", baseline.get("snapshot_sha256"),
                    "git_guards_installed", installedGuards
                )
            );
            return state;
        } catch (RuntimeException failure) {
            if (lockAcquired) {
                try {
                    removeInitializationFiles(paths.get("control"));
                    releaseLock(repoRoot, featureDir, featureId);
                } catch (RuntimeException rollback) {
                    throw new ControlError(failure.getMessage()
                        + "; initialization rollback failed: " + rollback.getMessage(), failure);
                }
            }
            throw failure;
        }
    }

    static Map<String, Object> cmdMigrateLegacy(Opts args) {
        Path featureDir = normalizeFeatureDir(args.required("--feature-dir"));
        Map<String, Path> paths = featurePaths(featureDir);
        if (Files.exists(paths.get("state"))) {
            throw new ControlError("Legacy feature already has control state");
        }
        Path repoRoot = gitRoot(featureDir);
        Map<String, Object> artifacts = new LinkedHashMap<String, Object>();
        for (Map.Entry<String, String> entry : ARTIFACT_FILES.entrySet()) {
            Path path = featureDir.resolve(entry.getValue());
            if (!Files.isRegularFile(path)) continue;
            String digest = sha256File(path);
            artifacts.put(
                entry.getKey(),
                map(
                    "path", entry.getValue(),
                    "revision", 1L,
                    "sha256", digest,
                    "snapshot_path", persistArtifactSnapshot(
                        featureDir, entry.getKey(), 1, digest
                    ),
                    "status", "historical-record",
                    "recorded_at", utcNow()
                )
            );
        }
        String featureRepoPath = relative(repoRoot, featureDir);
        Map<String, Object> blocked = map(
            "code", "LEGACY_APPROVAL_EVIDENCE_UNVERIFIED",
            "reason", "Historical AI review records are not valid human approvals.",
            "recovery", "Run a new SDD2 attempt from a current brief; do not resume this example."
        );
        Map<String, Object> state = map(
            "schema_version", SCHEMA_VERSION,
            "feature_id", args.required("--feature-id"),
            "feature_dir", featureRepoPath,
            "feature_repo_path", featureRepoPath,
            "execution_mode", "historical-example",
            "entry_contract", map(
                "user_entry", "brief-prompt-and-skill-call",
                "developer_action_required", false,
                "version", 1L
            ),
            "workspace_binding", map(
                "repo_root", ".",
                "worktree", ".",
                "repository_id", repositoryId(repoRoot),
                "branch", runGit(repoRoot, "branch", "--show-current")
            ),
            "revision", 1L,
            "attempt", 1L,
            "current_stage", "archive",
            "stage_status", "superseded",
            "last_completed_stage", null,
            "next_required_action", "none-historical-example",
            "blocked", blocked,
            "artifacts", artifacts,
            "approvals", new LinkedHashMap<String, Object>(),
            "quality_gates", new LinkedHashMap<String, Object>(),
            "required_phases", new ArrayList<Object>(),
            "phase_reviews", new LinkedHashMap<String, Object>(),
            "invalidations", new ArrayList<Object>(),
            "demo_authorization", null,
            "planning_baseline", null,
            "implementation_started", false,
            "implementation_permit", null,
            "implementation_permit_history", new ArrayList<Object>(),
            "unit_test_execution", null,
            "created_at", utcNow(),
            "updated_at", utcNow()
        );
        try {
            Files.createDirectories(paths.get("control"));
            if (!Files.exists(paths.get("approvals"))) {
                Files.createFile(paths.get("approvals"));
            }
            if (!Files.exists(paths.get("events"))) {
                Files.createFile(paths.get("events"));
            }
        } catch (IOException exc) {
            throw new ControlError("Cannot initialize legacy Feature control files", exc);
        }
        saveState(featureDir, state);
        appendEvent(
            featureDir, state, "legacy-example-quarantined",
            map("reason", blocked.get("code"))
        );
        return state;
    }

    static Map<String, Object> cmdAuthorizeDemo(Opts args) {
        Path featureDir = normalizeFeatureDir(args.required("--feature-dir"));
        Map<String, Object> state = loadState(featureDir);
        if (!"demo".equals(text(state, "execution_mode"))) {
            throw new ControlError(
                "Demo authorization is only valid when execution_mode=demo"
            );
        }
        assertControlIntegrity(featureDir, state, null, false);
        String authorizationText = args.required("--authorization-text");
        String lowered = authorizationText.toLowerCase(Locale.ROOT);
        if (!containsAny(lowered, DEMO_TERMS)
            || containsAny(lowered, DEMO_REJECTION_TERMS)
            || !containsAny(lowered, DEMO_ACTION_TERMS)) {
            throw new ControlError(
                "Demo authorization text must explicitly identify a demo/simulation"
            );
        }
        Map<String, Object> authorization = map(
            "source", "user-message",
            "message_id", args.one("--message-id", null),
            "authorization_text", authorizationText,
            "authorized_at", utcNow()
        );
        state.put("demo_authorization", authorization);
        incrementRevision(state);
        appendEvent(featureDir, state, "demo-authorized", authorization);
        saveState(featureDir, state);
        return state;
    }

    static Map<String, Object> cmdRecordArtifact(Opts args) {
        Path featureDir = normalizeFeatureDir(args.required("--feature-dir"));
        Map<String, Object> state = loadState(featureDir);
        if ("historical-example".equals(text(state, "execution_mode"))) {
            throw new ControlError(
                "Historical examples are immutable and cannot progress"
            );
        }
        String stage = args.required("--stage");
        if (!ARTIFACT_FILES.containsKey(stage)) {
            throw new ControlError("Unknown artifact stage: " + stage);
        }
        if (TERMINAL_STATUSES.contains(text(state, "stage_status"))) {
            throw new ControlError(
                "Terminal SDD2 attempts are immutable; restart a new attempt explicitly"
            );
        }
        assertControlIntegrity(featureDir, state, stage, true);
        Path path = featureDir.resolve(ARTIFACT_FILES.get(stage));
        validateArtifactLanguage(path, stage);
        String digest = sha256File(path);
        Map<String, Object> artifacts = object(state.get("artifacts"));
        Map<String, Object> previous = artifacts.get(stage) instanceof Map<?, ?>
            ? object(artifacts.get(stage))
            : null;
        String scopeSha256 = null;
        if (setOf(
            "code-review-findings", "auto-fix-summary",
            "unit-test-summary", "archive"
        ).contains(stage)) {
            List<Map<String, Object>> pair = requireCurrentScope(featureDir, state);
            scopeSha256 = text(pair.get(1), "snapshot_sha256");
        }
        if (previous != null && digest.equals(text(previous, "sha256"))) {
            if (scopeSha256 != null
                && !scopeSha256.equals(text(previous, "scope_sha256"))) {
                throw new ControlError(
                    stage + " still describes an older implementation scope; "
                    + "update the artifact for the current scope"
                );
            }
            return state;
        }
        assertArtifactEntry(featureDir, state, stage, previous);
        long revision = previous == null
            ? 1
            : integer(previous.get("revision"), 0) + 1;
        String snapshotPath = persistArtifactSnapshot(
            featureDir, stage, revision, digest
        );
        incrementRevision(state);
        List<String> invalidated = new ArrayList<String>();
        boolean permitRevoked = false;
        if (previous != null) {
            String reason = stage + " changed from revision "
                + previous.get("revision") + " to " + revision;
            invalidated = invalidateFrom(
                state, workflowStageForArtifact(stage), reason
            );
            if (setOf(
                "brief-design", "proposal-input", "spec", "design", "tasks"
            ).contains(stage)) {
                permitRevoked = revokeImplementationPermit(
                    featureDir, state, reason
                );
            }
        }
        Map<String, Object> record = map(
            "path", ARTIFACT_FILES.get(stage),
            "revision", revision,
            "sha256", digest,
            "snapshot_path", snapshotPath,
            "status", "recorded",
            "recorded_at", utcNow()
        );
        if (scopeSha256 != null) record.put("scope_sha256", scopeSha256);
        artifacts.put(stage, record);
        Map<String, List<String>> nextActions = new LinkedHashMap<String, List<String>>();
        nextActions.put("brief-design", listOf("proposal-input", "ready", "assemble-proposal-input"));
        nextActions.put("proposal-input", listOf("spec", "ready", "generate-spec"));
        nextActions.put("spec", listOf("spec", "awaiting-approval", "request-spec-approval"));
        nextActions.put("design", listOf("design", "awaiting-approval", "request-design-approval"));
        nextActions.put("tasks", listOf("tasks", "awaiting-approval", "request-tasks-approval"));
        nextActions.put("code-review-findings", listOf("code-review", "recorded", "record-code-review-gate"));
        nextActions.put("auto-fix-summary", listOf("auto-fix", "recorded", "record-auto-fix-gate"));
        nextActions.put("unit-test-summary", listOf("unit-test-summary", "recorded", "record-unit-test-gate"));
        nextActions.put("archive", listOf("archive", "awaiting-final-approval", "request-archive-approval"));
        List<String> transition = nextActions.get(stage);
        state.put("current_stage", transition.get(0));
        state.put("stage_status", transition.get(1));
        state.put("next_required_action", transition.get(2));
        appendEvent(
            featureDir, state, "artifact-recorded",
            map(
                "stage", stage,
                "artifact_revision", revision,
                "sha256", digest,
                "invalidated", invalidated,
                "implementation_permit_revoked", permitRevoked
            )
        );
        saveState(featureDir, state);
        return state;
    }

    static Map<String, Object> cmdApprove(Opts args) {
        Path featureDir = normalizeFeatureDir(args.required("--feature-dir"));
        Map<String, Object> state = loadState(featureDir);
        assertControlIntegrity(featureDir, state, null, false);
        String stage = args.required("--stage");
        if (!APPROVAL_STAGES.contains(stage)) {
            throw new ControlError("Stage does not accept approval: " + stage);
        }
        Map<String, Object> artifacts = object(state.get("artifacts"));
        if (!artifacts.containsKey(stage)) {
            throw new ControlError(
                "Cannot approve missing artifact: " + ARTIFACT_FILES.get(stage)
            );
        }
        String expectedStatus = "archive".equals(stage)
            ? "awaiting-final-approval"
            : "awaiting-approval";
        if (!stage.equals(text(state, "current_stage"))
            || !expectedStatus.equals(text(state, "stage_status"))) {
            throw new ControlError(
                "Approval is not current: expected " + stage + "/"
                + expectedStatus + ", found " + text(state, "current_stage")
                + "/" + text(state, "stage_status")
            );
        }
        String messageId = args.one("--message-id", null);
        if (messageId != null) {
            for (Map<String, Object> record :
                readJsonl(featurePaths(featureDir).get("approvals"))) {
                if (messageId.equals(text(record, "message_id"))) {
                    throw new ControlError(
                        "This user message ID has already been used for an SDD2 approval"
                    );
                }
            }
        }
        Map<String, Object> artifact = object(artifacts.get(stage));
        if (!currentArtifactHash(featureDir, stage).equals(
            text(artifact, "sha256")
        )) {
            throw new ControlError(
                "Artifact drift detected before approval: " + stage
            );
        }
        String source = args.required("--source");
        String approverRole = args.required("--approver-role");
        String approvalText = args.required("--approval-text");
        if (!explicitApproval(stage, approvalText)) {
            throw new ControlError(
                "Approval text is ambiguous or does not identify the "
                + stage + " stage"
            );
        }
        if ("user-message".equals(source)) {
            if (!setOf("human", "user").contains(approverRole)) {
                throw new ControlError(
                    "A real user-message approval must use approver_role=human or user"
                );
            }
        } else if ("demo-simulation".equals(source)) {
            if (!"demo".equals(text(state, "execution_mode"))
                || state.get("demo_authorization") == null) {
                throw new ControlError(
                    "AI demo approval requires prior explicit user demo authorization"
                );
            }
            if (!"ai-as-human-reviewer".equals(approverRole)) {
                throw new ControlError(
                    "Demo simulation must identify approver_role=ai-as-human-reviewer"
                );
            }
        } else {
            throw new ControlError("Unsupported approval source: " + source);
        }
        if ("archive".equals(stage)) {
            List<String> errors = archiveErrors(featureDir, state, true).stream()
                .filter(value -> !"APPROVAL_MISSING_OR_INVALID:archive".equals(value))
                .collect(Collectors.toList());
            if (!errors.isEmpty()) {
                throw new ControlError(
                    "Archive cannot be approved: " + String.join(", ", errors)
                );
            }
        }
        if ("unit-test-summary".equals(stage)) {
            Map<String, Object> unitGate = objectOrEmpty(
                objectOrEmpty(state.get("quality_gates")).get("unit-test")
            );
            if (!"passed".equals(text(unitGate, "status"))
                || !Objects.equals(
                    unitGate.get("artifact_sha256"), artifact.get("sha256")
                )
                || !Objects.equals(
                    unitGate.get("scope_sha256"), artifact.get("scope_sha256")
                )) {
                throw new ControlError(
                    "Unit Test Summary approval requires a passed Unit Test gate "
                    + "on this artifact and scope"
                );
            }
        }
        Map<String, Object> approval = appendChainedRecord(
            featurePaths(featureDir).get("approvals"),
            map(
                "approval_id", UUID.randomUUID().toString(),
                "timestamp", utcNow(),
                "feature_id", state.get("feature_id"),
                "attempt", state.get("attempt"),
                "stage", stage,
                "result", "approved",
                "source", source,
                "approver_role", approverRole,
                "message_id", messageId,
                "approval_text", approvalText,
                "artifact_path", artifact.get("path"),
                "artifact_revision", artifact.get("revision"),
                "artifact_sha256", artifact.get("sha256")
            ),
            "record_hash"
        );
        object(state.get("approvals")).put(
            stage,
            map(
                "approval_id", approval.get("approval_id"),
                "status", "approved",
                "attempt", state.get("attempt"),
                "artifact_revision", artifact.get("revision"),
                "artifact_sha256", artifact.get("sha256"),
                "record_hash", approval.get("record_hash"),
                "approved_at", approval.get("timestamp")
            )
        );
        Map<String, List<String>> transitions =
            new LinkedHashMap<String, List<String>>();
        transitions.put("spec", listOf("design", "ready", "generate-design"));
        transitions.put("design", listOf("tasks", "ready", "generate-tasks"));
        transitions.put("tasks", listOf("implementation", "ready", "capture-implementation-scope"));
        transitions.put("unit-test-summary", listOf("archive", "ready", "run-archive-check"));
        transitions.put("archive", listOf("archive", "completed", "none"));
        List<String> transition = transitions.get(stage);
        state.put("current_stage", transition.get(0));
        state.put("stage_status", transition.get(1));
        state.put("next_required_action", transition.get(2));
        state.put("last_completed_stage", stage);
        incrementRevision(state);
        appendEvent(
            featureDir, state, "stage-approved",
            map(
                "stage", stage,
                "approval_id", approval.get("approval_id"),
                "artifact_sha256", artifact.get("sha256")
            )
        );
        saveState(featureDir, state);
        if ("archive".equals(stage)) {
            releaseLock(
                stateRepoRoot(featureDir, state),
                featureDir,
                text(state, "feature_id")
            );
        }
        return state;
    }

    static Map<String, Object> cmdCaptureScope(Opts args) {
        Path featureDir = normalizeFeatureDir(args.required("--feature-dir"));
        Map<String, Object> state = loadState(featureDir);
        assertControlIntegrity(featureDir, state, null, true);
        if (!"implementation".equals(text(state, "current_stage"))
            || !"ready".equals(text(state, "stage_status"))) {
            throw new ControlError(
                "Implementation scope capture is only allowed immediately "
                + "after current Tasks approval"
            );
        }
        List<String> errors = approvalErrors(featureDir, state, "tasks");
        if (!errors.isEmpty()) {
            throw new ControlError(
                "Tasks approval is required before implementation: "
                + String.join(", ", errors)
            );
        }
        List<String> allowedPaths = args.many("--allowed-path");
        List<String> forbiddenPaths = args.many("--forbidden-path");
        List<String> requiredPhases = args.many("--required-phase");
        List<String> testPaths = args.many("--test-path");
        if (allowedPaths.isEmpty()) {
            throw new ControlError(
                "Implementation scope requires at least one allowed path"
            );
        }
        rejectUnsafePatterns(allowedPaths);
        rejectUnsafePatterns(forbiddenPaths);
        rejectUnsafePatterns(testPaths);
        if (requiredPhases.isEmpty()) {
            throw new ControlError(
                "Implementation scope requires at least one approved phase"
            );
        }
        Path repoRoot = stateRepoRoot(featureDir, state);
        String branch = runGit(repoRoot, "branch", "--show-current");
        String expectedBranch = text(
            object(state.get("workspace_binding")), "branch"
        );
        if (!branch.equals(expectedBranch)) {
            throw new ControlError(
                "Git branch changed since feature initialization"
            );
        }
        String baseCommit = args.one(
            "--base-commit", runGit(repoRoot, "rev-parse", "HEAD")
        );
        runGit(repoRoot, "cat-file", "-e", baseCommit + "^{commit}");
        List<String> effectiveTestPaths = testPaths.isEmpty()
            ? DEFAULT_TEST_PATHS
            : testPaths;
        Map<String, Object> scope = map(
            "schema_version", SCHEMA_VERSION,
            "feature_id", state.get("feature_id"),
            "attempt", state.get("attempt"),
            "repo_root", ".",
            "repository_id", repositoryId(repoRoot),
            "feature_repo_path", state.get("feature_repo_path"),
            "branch", branch,
            "base_commit", baseCommit,
            "allowed_paths", sortedUnique(allowedPaths),
            "forbidden_paths", sortedUnique(forbiddenPaths),
            "required_phases", uniqueInOrder(requiredPhases),
            "production_change", !args.flag("--non-production-change"),
            "test_path_patterns", sortedUnique(effectiveTestPaths),
            "captured_at", utcNow(),
            "code_revision", 0L,
            "frozen_snapshot", null
        );
        Map<String, Object> initial = snapshotForScope(repoRoot, scope);
        List<String> violations = stringList(initial.get("violations"));
        if (!violations.isEmpty()) {
            throw new ControlError(
                "Pre-existing scope violations: "
                + String.join(", ", violations)
            );
        }
        List<Object> initialFiles = arrayOrEmpty(initial.get("files"));
        if (!initialFiles.isEmpty()) {
            String dirty = initialFiles.stream()
                .limit(10)
                .map(item -> text(object(item), "path"))
                .collect(Collectors.joining(", "));
            throw new ControlError(
                "Implementation scope must start from a clean baseline; "
                + "pre-existing changes found: " + dirty
            );
        }
        scope.put("initial_snapshot", initial);
        Map<String, Object> permit = issueImplementationPermit(
            featureDir, state, scope
        );
        atomicWriteJson(featurePaths(featureDir).get("scope"), scope);
        state.put("implementation_started", true);
        state.put("implementation_permit", permit);
        state.put("required_phases", scope.get("required_phases"));
        state.put("current_stage", "implementation");
        state.put("stage_status", "executing");
        state.put("next_required_action", "implement-next-approved-phase");
        incrementRevision(state);
        appendEvent(
            featureDir, state, "implementation-scope-captured",
            map(
                "base_commit", baseCommit,
                "allowed_paths", scope.get("allowed_paths"),
                "required_phases", scope.get("required_phases"),
                "implementation_permit_sha256", permit.get("permit_sha256")
            )
        );
        saveState(featureDir, state);
        return scope;
    }

    static String workflowStageForArtifact(String stage) {
        if ("code-review-findings".equals(stage)) return "code-review";
        if ("auto-fix-summary".equals(stage)) return "auto-fix";
        return stage;
    }

    static void deleteIfExists(Path path) {
        try {
            Files.deleteIfExists(path);
        } catch (IOException exc) {
            throw new ControlError("Cannot remove stale control file: " + path, exc);
        }
    }

    static List<Map<String, Object>> requireCurrentScope(
        Path featureDir, Map<String, Object> state
    ) {
        Map<String, Object> scope = loadScope(featureDir);
        assertImplementationPermit(featureDir, state, scope);
        Map<String, Object> snapshot = snapshotForScope(
            scopeRepoRoot(featureDir, scope), scope
        );
        List<String> violations = stringList(snapshot.get("violations"));
        if (!violations.isEmpty()) {
            throw new ControlError(
                "Scope violation: " + String.join(", ", violations)
            );
        }
        Map<String, Object> frozen = objectOrEmpty(scope.get("frozen_snapshot"));
        if (frozen.isEmpty()
            || !Objects.equals(
                frozen.get("snapshot_sha256"), snapshot.get("snapshot_sha256")
            )) {
            throw new ControlError(
                "Implementation scope changed; run freeze-scope and re-enter Code Review"
            );
        }
        return listOf(scope, snapshot);
    }

    static Map<String, Object> cmdPhaseReview(Opts args) {
        Path featureDir = normalizeFeatureDir(args.required("--feature-dir"));
        Map<String, Object> state = loadState(featureDir);
        assertControlIntegrity(featureDir, state, null, true);
        if (!"implementation".equals(text(state, "current_stage"))) {
            throw new ControlError(
                "Phase Review is only valid during implementation"
            );
        }
        String phase = args.required("--phase");
        List<String> requiredPhases = stringList(state.get("required_phases"));
        if (!requiredPhases.contains(phase)) {
            throw new ControlError(
                "Phase is not declared in implementation scope: " + phase
            );
        }
        Map<String, Object> phaseReviews = object(state.get("phase_reviews"));
        String nextPhase = null;
        for (String candidate : requiredPhases) {
            Map<String, Object> review = objectOrEmpty(phaseReviews.get(candidate));
            if (!"approved".equals(text(review, "status"))) {
                nextPhase = candidate;
                break;
            }
        }
        if (!Objects.equals(nextPhase, phase)) {
            throw new ControlError(
                "Phase Review order violation: expected " + nextPhase
                + ", received " + phase
            );
        }
        String approvalText = args.required("--approval-text");
        if (!directApproval(
            approvalText, listOf(phase, "phase review", "阶段")
        )) {
            throw new ControlError(
                "Phase approval must identify the phase and explicit approval result"
            );
        }
        String messageId = args.one("--message-id", null);
        if (messageId != null) {
            for (Map<String, Object> record :
                readJsonl(featurePaths(featureDir).get("approvals"))) {
                if (messageId.equals(text(record, "message_id"))) {
                    throw new ControlError(
                        "This user message ID has already been used for an SDD2 approval"
                    );
                }
            }
            for (Object value : phaseReviews.values()) {
                if (messageId.equals(text(objectOrEmpty(value), "message_id"))) {
                    throw new ControlError(
                        "This user message ID has already been used for an SDD2 approval"
                    );
                }
            }
        }
        String source = args.required("--source");
        String approverRole = args.required("--approver-role");
        if ("user-message".equals(source)) {
            if (!setOf("human", "user").contains(approverRole)) {
                throw new ControlError(
                    "A real user-message Phase Review must use approver_role=human or user"
                );
            }
        } else if ("demo-simulation".equals(source)) {
            if (!"demo".equals(text(state, "execution_mode"))
                || state.get("demo_authorization") == null) {
                throw new ControlError(
                    "AI demo Phase Review requires prior explicit user demo authorization"
                );
            }
            if (!"ai-as-human-reviewer".equals(approverRole)) {
                throw new ControlError(
                    "Demo simulation must identify approver_role=ai-as-human-reviewer"
                );
            }
        } else {
            throw new ControlError(
                "Unsupported Phase Review source: " + source
            );
        }
        Map<String, Object> tasksArtifact = object(
            object(state.get("artifacts")).get("tasks")
        );
        Map<String, Object> approval = appendChainedRecord(
            featurePaths(featureDir).get("approvals"),
            map(
                "approval_id", UUID.randomUUID().toString(),
                "timestamp", utcNow(),
                "feature_id", state.get("feature_id"),
                "attempt", state.get("attempt"),
                "stage", "phase-review:" + phase,
                "result", "approved",
                "source", source,
                "approver_role", approverRole,
                "message_id", messageId,
                "approval_text", approvalText,
                "artifact_path", tasksArtifact.get("path"),
                "artifact_revision", tasksArtifact.get("revision"),
                "artifact_sha256", tasksArtifact.get("sha256")
            ),
            "record_hash"
        );
        phaseReviews.put(
            phase,
            map(
                "approval_id", approval.get("approval_id"),
                "record_hash", approval.get("record_hash"),
                "attempt", state.get("attempt"),
                "status", "approved",
                "source", source,
                "approver_role", approverRole,
                "message_id", messageId,
                "approval_text", approvalText,
                "approved_at", utcNow(),
                "tasks_revision", tasksArtifact.get("revision"),
                "tasks_sha256", tasksArtifact.get("sha256")
            )
        );
        incrementRevision(state);
        List<String> remaining = new ArrayList<String>();
        for (String candidate : requiredPhases) {
            if (!"approved".equals(
                text(objectOrEmpty(phaseReviews.get(candidate)), "status")
            )) {
                remaining.add(candidate);
            }
        }
        state.put("stage_status", "executing");
        state.put(
            "next_required_action",
            remaining.isEmpty()
                ? "freeze-implementation-scope"
                : "implement-phase:" + remaining.get(0)
        );
        appendEvent(
            featureDir, state, "phase-approved",
            map(
                "phase", phase,
                "source", source,
                "approver_role", approverRole
            )
        );
        saveState(featureDir, state);
        return state;
    }

    static Map<String, Object> cmdFreezeScope(Opts args) {
        Path featureDir = normalizeFeatureDir(args.required("--feature-dir"));
        Map<String, Object> state = loadState(featureDir);
        assertControlIntegrity(featureDir, state, null, true);
        String currentStage = text(state, "current_stage");
        if (!setOf(
            "implementation", "code-review", "auto-fix", "unit-test-summary"
        ).contains(currentStage)) {
            throw new ControlError(
                "Scope freeze is not valid from current stage " + currentStage
            );
        }
        for (String phase : stringList(state.get("required_phases"))) {
            List<String> errors = phaseReviewErrors(featureDir, state, phase);
            if (!errors.isEmpty()) {
                throw new ControlError(
                    "Scope freeze requires current Phase Review approval: "
                    + String.join(", ", errors)
                );
            }
        }
        Map<String, Object> scope = loadScope(featureDir);
        Map<String, Object> snapshot = snapshotForScope(
            scopeRepoRoot(featureDir, scope), scope
        );
        List<String> violations = stringList(snapshot.get("violations"));
        if (!violations.isEmpty()) {
            state.put(
                "blocked",
                map(
                    "code", "IMPLEMENTATION_SCOPE_VIOLATION",
                    "reason", String.join(", ", violations),
                    "recovery", "Return to tasks scope approval or remove unrelated changes."
                )
            );
            state.put("stage_status", "blocked");
            state.put("next_required_action", "resolve-scope-violation");
            state.put("unit_test_execution", null);
            deleteIfExists(featurePaths(featureDir).get("unit_test_evidence"));
            incrementRevision(state);
            appendEvent(
                featureDir, state,
                "implementation-scope-violation-blocked",
                map("violations", violations)
            );
            saveState(featureDir, state);
            throw new ControlError(
                "Implementation scope violation: "
                + String.join(", ", violations)
            );
        }
        Map<String, Object> previous = objectOrEmpty(
            scope.get("frozen_snapshot")
        );
        List<String> invalidated;
        if (previous.isEmpty()
            || !Objects.equals(
                previous.get("snapshot_sha256"),
                snapshot.get("snapshot_sha256")
            )) {
            long codeRevision = integer(scope.get("code_revision"), 0) + 1;
            scope.put("code_revision", codeRevision);
            invalidated = invalidateFrom(
                state, "code-review", "Implementation snapshot changed"
            );
            state.put("unit_test_execution", null);
            deleteIfExists(featurePaths(featureDir).get("unit_test_evidence"));
            deleteIfExists(featurePaths(featureDir).get("archive_evidence"));
        } else {
            invalidated = new ArrayList<String>();
        }
        snapshot.put("code_revision", scope.get("code_revision"));
        scope.put("frozen_snapshot", snapshot);
        atomicWriteJson(featurePaths(featureDir).get("scope"), scope);
        state.put("blocked", null);
        state.put("current_stage", "code-review");
        state.put("stage_status", "ready");
        state.put("next_required_action", "run-code-review");
        incrementRevision(state);
        appendEvent(
            featureDir, state, "implementation-scope-frozen",
            map(
                "scope_sha256", snapshot.get("snapshot_sha256"),
                "code_revision", scope.get("code_revision"),
                "invalidated", invalidated
            )
        );
        saveState(featureDir, state);
        return snapshot;
    }

    static Map<String, Object> cmdRunUnitTest(Opts args) {
        Path featureDir = normalizeFeatureDir(args.required("--feature-dir"));
        Map<String, Object> state = loadState(featureDir);
        assertControlIntegrity(featureDir, state, null, false);
        String nextAction = text(state, "next_required_action");
        if (!"unit-test-summary".equals(text(state, "current_stage"))
            || !"ready".equals(text(state, "stage_status"))
            || !setOf(
                "generate-or-update-test-source",
                "generate-unit-test-summary-from-evidence"
            ).contains(nextAction)) {
            throw new ControlError(
                "Observed Unit Test execution is only valid after current "
                + "Code Review and Auto-fix are closed"
            );
        }
        long timeoutSeconds = args.longValue("--timeout-seconds", 600);
        if (timeoutSeconds < 1 || timeoutSeconds > 3600) {
            throw new ControlError(
                "Unit Test timeout must be between 1 and 3600 seconds"
            );
        }
        List<Map<String, Object>> pair = requireCurrentScope(featureDir, state);
        Map<String, Object> scope = pair.get(0);
        Map<String, Object> beforeSnapshot = pair.get(1);
        String currentSha = text(beforeSnapshot, "snapshot_sha256");
        Map<String, Object> gates = objectOrEmpty(state.get("quality_gates"));
        Map<String, Object> review = objectOrEmpty(gates.get("code-review"));
        Map<String, Object> autoFix = objectOrEmpty(gates.get("auto-fix"));
        if (!"passed".equals(text(review, "status"))
            || !currentSha.equals(text(review, "scope_sha256"))) {
            throw new ControlError(
                "Unit Test execution requires Code Review passed on the current scope"
            );
        }
        if (!setOf("passed", "not-required").contains(
                text(autoFix, "status")
            )
            || !currentSha.equals(text(autoFix, "scope_sha256"))) {
            throw new ControlError(
                "Unit Test execution requires Auto-fix closed on the current scope"
            );
        }
        List<String> testSources = changedTestPaths(scope, beforeSnapshot);
        if (!Boolean.FALSE.equals(scope.get("production_change"))
            && testSources.isEmpty()) {
            throw new ControlError(
                "Unit Test execution requires at least one changed test source "
                + "matching the captured test path patterns"
            );
        }
        List<Object> testSourceRecords = new ArrayList<Object>();
        for (Object value : arrayOrEmpty(beforeSnapshot.get("files"))) {
            Map<String, Object> item = objectOrEmpty(value);
            if (testSources.contains(text(item, "path"))) {
                testSourceRecords.add(value);
            }
        }
        List<String> command = new ArrayList<String>(args.remainder());
        String runnerKind = testCommandKind(command);
        Path cwdValue = Paths.get(args.one("--cwd", "."));
        if (cwdValue.isAbsolute()) {
            throw new ControlError(
                "Unit Test cwd must be repository-relative"
            );
        }
        Path repoRoot = scopeRepoRoot(featureDir, scope);
        Path executionCwd = repoRoot.resolve(cwdValue).normalize();
        if (!executionCwd.startsWith(repoRoot)) {
            throw new ControlError("Unit Test cwd escapes the repository");
        }
        if (!Files.isDirectory(executionCwd)) {
            throw new ControlError(
                "Unit Test cwd does not exist: " + args.one("--cwd", ".")
            );
        }
        String startedAt = utcNow();
        String stdout = "";
        String stderr = "";
        Long exitCode = null;
        boolean timedOut = false;
        String launchError = null;
        try {
            Map<String, String> environment = null;
            if (runnerKind.startsWith("python")
                || "pytest".equals(runnerKind)) {
                environment = mapString(
                    "PYTHONDONTWRITEBYTECODE", "1"
                );
            }
            ProcResult process = runProcess(
                command, executionCwd, timeoutSeconds, environment
            );
            stdout = process.stdout;
            stderr = process.stderr;
            timedOut = process.timedOut;
            if (!timedOut) exitCode = (long) process.exitCode;
        } catch (ControlError exc) {
            launchError = exc.getClass().getSimpleName() + ": " + exc.getMessage();
        }
        String completedAt = utcNow();
        Map<String, Object> afterSnapshot = snapshotForScope(repoRoot, scope);
        boolean scopeChanged =
            !stringList(afterSnapshot.get("violations")).isEmpty()
            || !currentSha.equals(text(afterSnapshot, "snapshot_sha256"));
        Map<String, Object> counts = parsedTestCounts(stdout, stderr);
        String outcome;
        String failureReason = null;
        if (timedOut) {
            outcome = "blocked";
            failureReason = "TEST_EXECUTION_TIMEOUT";
        } else if (launchError != null) {
            outcome = "blocked";
            failureReason = "TEST_EXECUTION_LAUNCH_ERROR";
        } else if (scopeChanged) {
            outcome = "blocked";
            failureReason = "TEST_CHANGED_FROZEN_SCOPE";
        } else if (exitCode == null || exitCode.longValue() != 0
            || integer(counts.get("failed"), 0) > 0
            || integer(counts.get("errors"), 0) > 0) {
            outcome = "failed";
            failureReason = "TEST_EXECUTION_FAILED";
        } else if (integer(counts.get("total"), 0) <= 0
            || integer(counts.get("passed"), 0) <= 0) {
            outcome = "blocked";
            failureReason = "NO_EXECUTED_TEST_OBSERVED";
        } else {
            outcome = "passed";
        }
        String cwd = relative(repoRoot, executionCwd);
        if (cwd.isEmpty()) cwd = ".";
        Map<String, Object> evidence = map(
            "schema_version", SCHEMA_VERSION,
            "feature_id", state.get("feature_id"),
            "attempt", state.get("attempt"),
            "scope_sha256", currentSha,
            "scope_after_sha256", afterSnapshot.get("snapshot_sha256"),
            "scope_changed_during_test", scopeChanged,
            "scope_violations", afterSnapshot.get("violations"),
            "code_revision", scope.get("code_revision"),
            "runner_kind", runnerKind,
            "command", command,
            "cwd", cwd,
            "timeout_seconds", timeoutSeconds,
            "started_at", startedAt,
            "completed_at", completedAt,
            "exit_code", exitCode,
            "timed_out", timedOut,
            "launch_error", launchError,
            "stdout_sha256", sha256Bytes(
                stdout.getBytes(StandardCharsets.UTF_8)
            ),
            "stderr_sha256", sha256Bytes(
                stderr.getBytes(StandardCharsets.UTF_8)
            ),
            "stdout_excerpt", boundedOutput(stdout, 12000),
            "stderr_excerpt", boundedOutput(stderr, 12000),
            "test_counts", counts,
            "changed_test_paths", testSources,
            "changed_test_sources", testSourceRecords,
            "outcome", outcome,
            "failure_reason", failureReason
        );
        evidence.put(
            "evidence_sha256",
            sha256Bytes(canonicalJson(evidence).getBytes(StandardCharsets.UTF_8))
        );
        atomicWriteJson(
            featurePaths(featureDir).get("unit_test_evidence"), evidence
        );
        state.put(
            "unit_test_execution",
            map(
                "feature_id", state.get("feature_id"),
                "attempt", state.get("attempt"),
                "scope_sha256", currentSha,
                "code_revision", scope.get("code_revision"),
                "outcome", outcome,
                "evidence_sha256", evidence.get("evidence_sha256"),
                "recorded_at", completedAt
            )
        );
        if (scopeChanged) {
            String reason = String.join(
                ", ", stringList(afterSnapshot.get("violations"))
            );
            if (reason.isEmpty()) {
                reason = "Unit Test command changed the frozen implementation snapshot.";
            }
            state.put(
                "blocked",
                map(
                    "code", "UNIT_TEST_SCOPE_CHANGED",
                    "reason", reason,
                    "recovery", "Remove generated scope changes or approve and "
                        + "refreeze them, then rerun full review and tests."
                )
            );
            state.put("stage_status", "blocked");
            state.put("next_required_action", "resolve-unit-test");
        } else {
            state.put("blocked", null);
            state.put("current_stage", "unit-test-summary");
            state.put("stage_status", "ready");
            state.put(
                "next_required_action",
                "generate-unit-test-summary-from-evidence"
            );
        }
        incrementRevision(state);
        appendEvent(
            featureDir, state, "unit-test-executed",
            map(
                "evidence_sha256", evidence.get("evidence_sha256"),
                "scope_sha256", currentSha,
                "outcome", outcome,
                "exit_code", exitCode,
                "test_counts", counts
            )
        );
        saveState(featureDir, state);
        return evidence;
    }

    static Map<String, String> mapString(String... entries) {
        LinkedHashMap<String, String> result =
            new LinkedHashMap<String, String>();
        for (int index = 0; index < entries.length; index += 2) {
            result.put(entries[index], entries[index + 1]);
        }
        return result;
    }

    static Map<String, Object> cmdQualityGate(Opts args) {
        Path featureDir = normalizeFeatureDir(args.required("--feature-dir"));
        Map<String, Object> state = loadState(featureDir);
        assertControlIntegrity(featureDir, state, null, false);
        String gate = args.required("--gate");
        Map<String, String> expectedStages = linkedMap(
            "code-review", "code-review",
            "auto-fix", "auto-fix",
            "unit-test", "unit-test-summary"
        );
        if (!expectedStages.containsKey(gate)) {
            throw new ControlError("Unknown quality gate: " + gate);
        }
        String expectedStage = expectedStages.get(gate);
        if (!expectedStage.equals(text(state, "current_stage"))) {
            throw new ControlError(
                gate + " gate is not current: expected stage "
                + expectedStage + ", found " + text(state, "current_stage")
            );
        }
        if (!"recorded".equals(text(state, "stage_status"))) {
            throw new ControlError(
                gate + " gate requires its current artifact to be recorded first"
            );
        }
        List<Map<String, Object>> pair = requireCurrentScope(featureDir, state);
        Map<String, Object> scope = pair.get(0);
        Map<String, Object> snapshot = pair.get(1);
        String currentSha = text(snapshot, "snapshot_sha256");
        Map<String, Object> qualityGates = object(state.get("quality_gates"));
        Map<String, Object> artifacts = object(state.get("artifacts"));
        Set<String> allowed;
        if ("code-review".equals(gate)) {
            for (String stage : listOf("spec", "design", "tasks")) {
                List<String> errors = approvalErrors(
                    featureDir, state, stage
                );
                if (!errors.isEmpty()) {
                    throw new ControlError(
                        "Code Review blocked: " + String.join(", ", errors)
                    );
                }
            }
            for (String phase : stringList(state.get("required_phases"))) {
                List<String> errors = phaseReviewErrors(
                    featureDir, state, phase
                );
                if (!errors.isEmpty()) {
                    throw new ControlError(
                        "Code Review blocked: " + String.join(", ", errors)
                    );
                }
            }
            if (!artifacts.containsKey("code-review-findings")) {
                throw new ControlError(
                    "code-review-findings.md must be recorded before the Code Review gate"
                );
            }
            allowed = setOf("passed", "failed", "blocked");
        } else if ("auto-fix".equals(gate)) {
            Map<String, Object> review = objectOrEmpty(
                qualityGates.get("code-review")
            );
            if (!"passed".equals(text(review, "status"))
                || !currentSha.equals(text(review, "scope_sha256"))) {
                throw new ControlError(
                    "Auto-fix requires Code Review passed on the current scope"
                );
            }
            if (!artifacts.containsKey("auto-fix-summary")) {
                throw new ControlError(
                    "auto-fix-summary.md must be recorded before the Auto-fix gate"
                );
            }
            allowed = setOf(
                "passed", "not-required", "failed", "blocked"
            );
        } else {
            Map<String, Object> review = objectOrEmpty(
                qualityGates.get("code-review")
            );
            Map<String, Object> autoFix = objectOrEmpty(
                qualityGates.get("auto-fix")
            );
            if (!"passed".equals(text(review, "status"))
                || !currentSha.equals(text(review, "scope_sha256"))) {
                throw new ControlError(
                    "Unit Test requires Code Review passed on the current scope"
                );
            }
            if (!setOf("passed", "not-required").contains(
                    text(autoFix, "status")
                )
                || !currentSha.equals(text(autoFix, "scope_sha256"))) {
                throw new ControlError(
                    "Unit Test requires Auto-fix closed on the current scope"
                );
            }
            if (!artifacts.containsKey("unit-test-summary")) {
                throw new ControlError(
                    "unit-test-summary.md must be recorded before the Unit Test gate"
                );
            }
            if (!Boolean.FALSE.equals(scope.get("production_change"))
                && changedTestPaths(scope, snapshot).isEmpty()) {
                throw new ControlError(
                    "Unit Test requires at least one changed test source "
                    + "matching the captured test path patterns"
                );
            }
            allowed = setOf("passed", "failed", "blocked", "not-run");
        }
        String result = args.required("--result");
        if (!allowed.contains(result)) {
            throw new ControlError(
                "Invalid " + gate + " result: " + result
                + "; expected one of " + new TreeSet<String>(allowed)
            );
        }
        String evidenceText = args.required("--evidence");
        if (blank(evidenceText)) {
            throw new ControlError(
                gate + " requires non-empty reproducible evidence"
            );
        }
        if ("unit-test".equals(gate)
            && setOf("passed", "failed").contains(result)) {
            List<String> errors = unitTestExecutionErrors(
                featureDir, state, result
            );
            if (!errors.isEmpty()) {
                throw new ControlError(
                    "Unit Test gate requires controller-observed execution: "
                    + String.join(", ", errors)
                );
            }
            Map<String, Object> execution = objectOrEmpty(
                state.get("unit_test_execution")
            );
            if (!currentSha.equals(text(execution, "scope_sha256"))) {
                throw new ControlError(
                    "Unit Test execution evidence belongs to a different "
                    + "implementation scope"
                );
            }
        }
        Map<String, Object> record = map(
            "status", result,
            "recorded_at", utcNow(),
            "scope_sha256", currentSha,
            "code_revision", scope.get("code_revision"),
            "evidence", evidenceText
        );
        Map<String, String> artifactStages = linkedMap(
            "code-review", "code-review-findings",
            "auto-fix", "auto-fix-summary",
            "unit-test", "unit-test-summary"
        );
        Map<String, Object> artifact = object(
            artifacts.get(artifactStages.get(gate))
        );
        record.put("artifact_sha256", artifact.get("sha256"));
        if ("unit-test".equals(gate)) {
            record.put(
                "changed_test_paths", changedTestPaths(scope, snapshot)
            );
            Map<String, Object> execution = objectOrEmpty(
                state.get("unit_test_execution")
            );
            if (execution.get("evidence_sha256") != null) {
                record.put(
                    "test_execution_sha256", execution.get("evidence_sha256")
                );
            }
        }
        qualityGates.put(gate, record);
        if ("code-review".equals(gate)) {
            if ("blocked".equals(result)) {
                state.put("stage_status", "blocked");
                state.put(
                    "blocked",
                    map(
                        "code", "CODE_REVIEW_BLOCKED",
                        "reason", evidenceText,
                        "recovery", "Resolve review input/scope evidence and rerun Code Review."
                    )
                );
                state.put("next_required_action", "resolve-code-review");
            } else {
                state.put("blocked", null);
                state.put("current_stage", "auto-fix");
                state.put("stage_status", "ready");
                state.put(
                    "next_required_action",
                    "failed".equals(result)
                        ? "apply-review-findings"
                        : "record-auto-fix-not-required-or-current-fixes"
                );
            }
        } else if ("auto-fix".equals(gate)) {
            if (setOf("failed", "blocked").contains(result)) {
                state.put("stage_status", "blocked");
                state.put(
                    "blocked",
                    map(
                        "code", "AUTO_FIX_"
                            + result.toUpperCase(Locale.ROOT),
                        "reason", evidenceText,
                        "recovery", "Resolve Auto-fix evidence or implementation "
                            + "and rerun from the current frozen scope."
                    )
                );
                state.put("next_required_action", "resolve-auto-fix");
            } else {
                state.put("blocked", null);
                state.put("current_stage", "unit-test-summary");
                state.put("stage_status", "ready");
                state.put(
                    "next_required_action",
                    "generate-or-update-test-source"
                );
            }
        } else if (!"passed".equals(result)) {
            state.put("stage_status", "blocked");
            state.put(
                "blocked",
                map(
                    "code", "UNIT_TEST_"
                        + result.toUpperCase(Locale.ROOT).replace('-', '_'),
                    "reason", evidenceText,
                    "recovery", "Fix/generate tests and implementation as needed, "
                        + "then refreeze, re-review, and rerun tests."
                )
            );
            state.put("next_required_action", "resolve-unit-test");
        } else {
            state.put("blocked", null);
            state.put("current_stage", "unit-test-summary");
            state.put("stage_status", "awaiting-approval");
            state.put(
                "next_required_action",
                "request-unit-test-summary-approval"
            );
        }
        incrementRevision(state);
        Map<String, Object> eventPayload =
            new LinkedHashMap<String, Object>();
        eventPayload.put("gate", gate);
        eventPayload.putAll(record);
        appendEvent(
            featureDir, state, "quality-gate-recorded", eventPayload
        );
        saveState(featureDir, state);
        return state;
    }

    static Map<String, Object> cmdValidate(Opts args) {
        Path featureDir = normalizeFeatureDir(args.required("--feature-dir"));
        Map<String, Object> state = loadState(featureDir);
        Map<String, Object> result = validateState(featureDir, state);
        List<String> errors = stringList(result.get("errors"));
        String nextStage = args.one("--next-stage", null);
        if (nextStage != null) {
            if (!STAGE_ORDER.contains(nextStage)) {
                throw new ControlError("Unknown next stage: " + nextStage);
            }
            if (APPROVAL_STAGES.contains(nextStage)
                && !"archive".equals(nextStage)) {
                Map<String, String> previousStages = linkedMap(
                    "design", "spec",
                    "tasks", "design",
                    "unit-test-summary", "tasks"
                );
                String previous = previousStages.get(nextStage);
                if (previous != null) {
                    errors.addAll(
                        approvalErrors(featureDir, state, previous)
                    );
                }
            }
            if ("archive".equals(nextStage)) {
                errors.addAll(archiveErrors(featureDir, state, false));
            }
        }
        errors = sortedUnique(errors);
        result.put("errors", errors);
        result.put("valid", errors.isEmpty());
        return result;
    }

    static Map<String, Object> cmdArchiveCheck(Opts args) {
        Path featureDir = normalizeFeatureDir(args.required("--feature-dir"));
        Map<String, Object> state = loadState(featureDir);
        List<String> errors = archiveErrors(
            featureDir, state, args.flag("--require-archive")
        );
        return map("valid", errors.isEmpty(), "errors", errors);
    }

    static Map<String, Object> cmdPrepareArchive(Opts args) {
        Path featureDir = normalizeFeatureDir(args.required("--feature-dir"));
        Map<String, Object> state = loadState(featureDir);
        assertControlIntegrity(featureDir, state, null, false);
        if (!"archive".equals(text(state, "current_stage"))
            || !"ready".equals(text(state, "stage_status"))) {
            throw new ControlError(
                "Archive evidence is only prepared after current Unit Test Summary approval"
            );
        }
        List<String> errors = new ArrayList<String>(
            approvalErrors(featureDir, state, "unit-test-summary")
        );
        Map<String, Path> paths = featurePaths(featureDir);
        if (Files.exists(paths.get("scope"))) {
            errors.addAll(qualityGateErrors(featureDir, state));
        } else {
            errors.add("SCOPE_MANIFEST_MISSING");
        }
        if (!errors.isEmpty()) {
            throw new ControlError(
                "Archive evidence cannot be prepared: "
                + String.join(", ", sortedUnique(errors))
            );
        }
        Map<String, Object> scope = loadScope(featureDir);
        Map<String, Object> frozen = objectOrEmpty(scope.get("frozen_snapshot"));
        if (frozen.isEmpty()) {
            throw new ControlError(
                "Archive evidence requires a frozen implementation scope"
            );
        }
        Map<String, Object> unitGate = object(
            object(state.get("quality_gates")).get("unit-test")
        );
        Map<String, Object> evidence = map(
            "schema_version", SCHEMA_VERSION,
            "feature_id", state.get("feature_id"),
            "attempt", state.get("attempt"),
            "branch", scope.get("branch"),
            "base_commit", scope.get("base_commit"),
            "head_commit", frozen.get("head_commit"),
            "head_tree", frozen.get("head_tree"),
            "scope_sha256", frozen.get("snapshot_sha256"),
            "unit_test_evidence_sha256",
                unitGate.get("test_execution_sha256"),
            "files", frozen.get("files")
        );
        Path existingPath = paths.get("archive_evidence");
        if (Files.isRegularFile(existingPath)) {
            Map<String, Object> existing = readJson(existingPath);
            Map<String, Object> comparable =
                new LinkedHashMap<String, Object>(existing);
            comparable.remove("generated_at");
            comparable.remove("evidence_sha256");
            if (comparable.equals(evidence)) {
                if ("generate-archive-from-evidence".equals(
                    text(state, "next_required_action")
                )) {
                    return existing;
                }
                evidence = existing;
            }
        }
        if (!evidence.containsKey("evidence_sha256")) {
            evidence.put("generated_at", utcNow());
            evidence.put(
                "evidence_sha256",
                sha256Bytes(
                    canonicalJson(evidence).getBytes(StandardCharsets.UTF_8)
                )
            );
            atomicWriteJson(existingPath, evidence);
        }
        incrementRevision(state);
        state.put("current_stage", "archive");
        state.put("stage_status", "ready");
        state.put("next_required_action", "generate-archive-from-evidence");
        appendEvent(
            featureDir, state, "archive-evidence-prepared",
            map(
                "evidence_sha256", evidence.get("evidence_sha256"),
                "scope_sha256", evidence.get("scope_sha256")
            )
        );
        saveState(featureDir, state);
        return evidence;
    }

    static Map<String, Object> cmdResume(Opts args) {
        Path featureDir = normalizeFeatureDir(args.required("--feature-dir"));
        Map<String, Object> state = loadState(featureDir);
        List<String> installedGuards = new ArrayList<String>();
        if (!"historical-example".equals(text(state, "execution_mode"))
            && !TERMINAL_STATUSES.contains(text(state, "stage_status"))) {
            Path repoRoot = stateRepoRoot(featureDir, state);
            acquireLock(
                repoRoot, featureDir, text(state, "feature_id")
            );
            installedGuards = installGitGuards(repoRoot);
            List<String> historyErrors = new ArrayList<String>(
                verifyLock(featureDir, state)
            );
            Map<String, Path> paths = featurePaths(featureDir);
            historyErrors.addAll(
                validateHashChain(paths.get("events"), "event_hash")
            );
            historyErrors.addAll(
                validateHashChain(paths.get("approvals"), "record_hash")
            );
            historyErrors.addAll(
                stateEventProjectionErrors(featureDir, state)
            );
            historyErrors.addAll(stateTransitionErrors(state));
            historyErrors.addAll(
                approvalProjectionErrors(featureDir, state)
            );
            historyErrors.addAll(
                workflowPrerequisiteErrors(featureDir, state, null)
            );
            historyErrors.addAll(
                qualityGateEventErrors(featureDir, state)
            );
            if (historyErrors.isEmpty()) {
                List<String> generationErrors = featureGenerationErrors(
                    featureDir, state, null
                );
                if (!generationErrors.isEmpty()) {
                    blockUnexpectedFeatureLayout(
                        featureDir, state, generationErrors
                    );
                } else {
                    Map<String, Object> blocked = objectOrEmpty(
                        state.get("blocked")
                    );
                    if (FEATURE_LAYOUT_BLOCK.equals(text(blocked, "code"))) {
                        restoreUnexpectedFeatureLayoutBlock(featureDir, state);
                    }
                    List<String> prematureErrors = planningGuardErrors(
                        featureDir, state
                    );
                    if (!prematureErrors.isEmpty()) {
                        blockPrematureImplementationChange(
                            featureDir, state, prematureErrors
                        );
                    } else {
                        blocked = objectOrEmpty(state.get("blocked"));
                        if (PREMATURE_CHANGE_BLOCK.equals(
                            text(blocked, "code")
                        )) {
                            restorePrematureChangeBlock(featureDir, state);
                        }
                    }
                }
            }
        }
        if (!"historical-example".equals(text(state, "execution_mode"))
            && TERMINAL_STATUSES.contains(text(state, "stage_status"))) {
            releaseTerminalLock(featureDir, state);
        }
        Map<String, Object> validation = validateState(featureDir, state);
        Map<String, Object> permit = objectOrEmpty(
            state.get("implementation_permit")
        );
        return map(
            "valid", stringList(validation.get("errors")).isEmpty(),
            "feature_id", state.get("feature_id"),
            "execution_mode", state.get("execution_mode"),
            "current_stage", state.get("current_stage"),
            "stage_status", state.get("stage_status"),
            "next_required_action", state.get("next_required_action"),
            "blocked", state.get("blocked"),
            "revision", state.get("revision"),
            "attempt", state.get("attempt"),
            "implementation_permit_status", permit.get("status"),
            "git_guards_installed", installedGuards,
            "validation", validation
        );
    }

    static Map<String, Object> cmdClose(Opts args) {
        Path featureDir = normalizeFeatureDir(args.required("--feature-dir"));
        Map<String, Object> state = loadState(featureDir);
        assertHistoryAndLock(featureDir, state);
        if (TERMINAL_STATUSES.contains(text(state, "stage_status"))) {
            if (Objects.equals(state.get("stage_status"), args.required("--result"))) {
                releaseTerminalLock(featureDir, state);
                return state;
            }
            throw new ControlError(
                "Terminal attempts are immutable; use restart-attempt for new work"
            );
        }
        String approvalText = args.required("--approval-text");
        String lowered = approvalText.toLowerCase(Locale.ROOT);
        if (!containsAny(
            lowered,
            listOf("风险", "risk", "终止", "abort", "关闭", "close")
        )) {
            throw new ControlError(
                "Closure approval must explicitly mention risk acceptance or abort/close"
            );
        }
        String result = args.required("--result");
        if (!setOf("closed-with-risk", "aborted").contains(result)) {
            throw new ControlError("Invalid closure result: " + result);
        }
        if ("closed-with-risk".equals(result)
            && state.get("blocked") == null) {
            throw new ControlError(
                "closed-with-risk is only valid for a recorded blocked/failed workflow"
            );
        }
        state.put("current_stage", "archive");
        state.put("stage_status", result);
        state.put("next_required_action", "none");
        incrementRevision(state);
        appendEvent(
            featureDir, state, "workflow-closed",
            map(
                "result", result,
                "source", "user-message",
                "message_id", args.one("--message-id", null),
                "approval_text", approvalText
            )
        );
        saveState(featureDir, state);
        releaseLock(
            stateRepoRoot(featureDir, state),
            featureDir,
            text(state, "feature_id")
        );
        return state;
    }

    static Map<String, Object> cmdRestartAttempt(Opts args) {
        Path featureDir = normalizeFeatureDir(args.required("--feature-dir"));
        Map<String, Object> state = loadState(featureDir);
        assertHistoryAndLock(featureDir, state);
        List<String> generationErrors = featureGenerationErrors(
            featureDir, state, null
        );
        if (!generationErrors.isEmpty()) {
            throw new ControlError(
                "Unexpected Feature paths must be removed before restart: "
                + String.join(", ", generationErrors)
            );
        }
        Map<String, Object> blocked = objectOrEmpty(state.get("blocked"));
        if (PREMATURE_CHANGE_BLOCK.equals(text(blocked, "code"))) {
            List<String> errors = planningGuardErrors(featureDir, state);
            if (!errors.isEmpty()) {
                throw new ControlError(
                    "Premature implementation changes must be restored before restart: "
                    + String.join(", ", errors)
                );
            }
        }
        if ("historical-example".equals(text(state, "execution_mode"))) {
            throw new ControlError(
                "Historical examples cannot start a new attempt"
            );
        }
        String stageStatus = text(state, "stage_status");
        if (!"blocked".equals(stageStatus)
            && !TERMINAL_STATUSES.contains(stageStatus)) {
            throw new ControlError(
                "A new attempt is only allowed after a blocked or terminal attempt"
            );
        }
        String approvalText = args.required("--approval-text");
        String lowered = approvalText.toLowerCase(Locale.ROOT);
        if (!containsAny(
            lowered, listOf("重试", "重新开始", "retry", "restart")
        )) {
            throw new ControlError(
                "New-attempt approval must explicitly request retry or restart"
            );
        }
        acquireLock(
            stateRepoRoot(featureDir, state),
            featureDir,
            text(state, "feature_id")
        );
        long oldAttempt = integer(state.get("attempt"), 0);
        state.put("attempt", oldAttempt + 1);
        incrementRevision(state);
        for (Object value : object(state.get("approvals")).values()) {
            Map<String, Object> approval = objectOrEmpty(value);
            approval.put("status", "invalidated");
            approval.put(
                "invalidated_reason",
                "Attempt " + oldAttempt + " ended; fresh approval is required"
            );
        }
        state.put(
            "quality_gates", new LinkedHashMap<String, Object>()
        );
        state.put(
            "phase_reviews", new LinkedHashMap<String, Object>()
        );
        state.put("required_phases", new ArrayList<Object>());
        if (state.get("implementation_permit") != null) {
            revokeImplementationPermit(
                featureDir, state, "Attempt " + oldAttempt + " ended"
            );
        }
        state.put(
            "planning_baseline",
            planningSnapshot(
                stateRepoRoot(featureDir, state),
                text(state, "feature_repo_path")
            )
        );
        state.put("implementation_started", false);
        state.put("implementation_permit", null);
        state.put("unit_test_execution", null);
        state.put("blocked", null);
        state.put("last_completed_stage", "brief-design");
        Map<String, Object> artifacts = object(state.get("artifacts"));
        if (artifacts.containsKey("spec")) {
            state.put("current_stage", "spec");
            state.put("stage_status", "awaiting-approval");
            state.put("next_required_action", "request-spec-approval");
        } else if (artifacts.containsKey("proposal-input")) {
            state.put("current_stage", "spec");
            state.put("stage_status", "ready");
            state.put("next_required_action", "generate-spec");
        } else {
            state.put("current_stage", "proposal-input");
            state.put("stage_status", "ready");
            state.put(
                "next_required_action", "assemble-proposal-input"
            );
        }
        Map<String, Path> paths = featurePaths(featureDir);
        deleteIfExists(paths.get("scope"));
        deleteIfExists(paths.get("unit_test_evidence"));
        deleteIfExists(paths.get("archive_evidence"));
        appendEvent(
            featureDir, state, "attempt-restarted",
            map(
                "previous_attempt", oldAttempt,
                "source", "user-message",
                "message_id", args.one("--message-id", null),
                "approval_text", approvalText
            )
        );
        saveState(featureDir, state);
        return state;
    }

    static void validateCommandOptions(String command, Opts args) {
        Set<String> values = new LinkedHashSet<String>();
        Set<String> flags = new LinkedHashSet<String>();
        boolean allowRemainder = false;
        if ("doctor".equals(command)) {
            values.add("--repo-root");
        } else if ("init".equals(command)) {
            values.addAll(setOf("--feature-dir", "--feature-id", "--mode"));
        } else if ("migrate-legacy".equals(command)) {
            values.addAll(setOf("--feature-dir", "--feature-id"));
        } else if ("authorize-demo".equals(command)) {
            values.addAll(setOf(
                "--feature-dir", "--authorization-text", "--message-id"
            ));
        } else if ("record-artifact".equals(command)) {
            values.addAll(setOf("--feature-dir", "--stage"));
        } else if ("approve".equals(command)) {
            values.addAll(setOf(
                "--feature-dir", "--stage", "--source", "--approver-role",
                "--approval-text", "--message-id"
            ));
        } else if ("capture-scope".equals(command)) {
            values.addAll(setOf(
                "--feature-dir", "--base-commit", "--allowed-path",
                "--forbidden-path", "--required-phase", "--test-path"
            ));
            flags.add("--non-production-change");
        } else if ("phase-review".equals(command)) {
            values.addAll(setOf(
                "--feature-dir", "--phase", "--source", "--approver-role",
                "--approval-text", "--message-id"
            ));
        } else if ("freeze-scope".equals(command)
            || "prepare-archive".equals(command)
            || "resume".equals(command)) {
            values.add("--feature-dir");
        } else if ("run-unit-test".equals(command)) {
            values.addAll(setOf(
                "--feature-dir", "--cwd", "--timeout-seconds"
            ));
            allowRemainder = true;
        } else if ("quality-gate".equals(command)) {
            values.addAll(setOf(
                "--feature-dir", "--gate", "--result", "--evidence"
            ));
        } else if ("validate".equals(command)) {
            values.addAll(setOf("--feature-dir", "--next-stage"));
        } else if ("archive-check".equals(command)) {
            values.add("--feature-dir");
            flags.add("--require-archive");
        } else if ("close".equals(command)) {
            values.addAll(setOf(
                "--feature-dir", "--result", "--approval-text", "--message-id"
            ));
        } else if ("restart-attempt".equals(command)) {
            values.addAll(setOf(
                "--feature-dir", "--approval-text", "--message-id"
            ));
        } else {
            throw new ControlError("Unknown command: " + command);
        }
        args.assertContract(values, flags, allowRemainder);
    }

    static Map<String, Object> dispatch(String command, Opts args) {
        validateCommandOptions(command, args);
        if ("doctor".equals(command)) return cmdDoctor(args);
        if ("init".equals(command)) return cmdInit(args);
        if ("migrate-legacy".equals(command)) return cmdMigrateLegacy(args);
        if ("authorize-demo".equals(command)) return cmdAuthorizeDemo(args);
        if ("record-artifact".equals(command)) return cmdRecordArtifact(args);
        if ("approve".equals(command)) return cmdApprove(args);
        if ("capture-scope".equals(command)) return cmdCaptureScope(args);
        if ("phase-review".equals(command)) return cmdPhaseReview(args);
        if ("freeze-scope".equals(command)) return cmdFreezeScope(args);
        if ("run-unit-test".equals(command)) return cmdRunUnitTest(args);
        if ("quality-gate".equals(command)) return cmdQualityGate(args);
        if ("validate".equals(command)) return cmdValidate(args);
        if ("archive-check".equals(command)) return cmdArchiveCheck(args);
        if ("prepare-archive".equals(command)) return cmdPrepareArchive(args);
        if ("resume".equals(command)) return cmdResume(args);
        if ("close".equals(command)) return cmdClose(args);
        if ("restart-attempt".equals(command)) {
            return cmdRestartAttempt(args);
        }
        throw new ControlError("Unknown command: " + command);
    }

    static int runMain(String[] argv) {
        if (argv.length == 0) {
            System.out.println(canonicalJson(map(
                "ok", false,
                "error", "缺少控制器命令。请通过 uaw-sdd-ai-coding Skill 启动流程。"
            )));
            return 2;
        }
        try {
            ensureRuntimeIntegrity();
            Map<String, Object> result = dispatch(
                argv[0], Opts.parse(argv, 1)
            );
            boolean ok = !Boolean.FALSE.equals(result.get("valid"));
            System.out.println(
                Json.pretty(map("ok", ok, "result", result))
            );
            return ok ? 0 : 1;
        } catch (ControlError exc) {
            System.out.println(canonicalJson(
                map("ok", false, "error", exc.getMessage())
            ));
            return 2;
        } catch (RuntimeException exc) {
            System.out.println(canonicalJson(
                map(
                    "ok", false,
                    "error", "SDD2_CONTROLLER_RUNTIME_FAILURE:控制器运行失败。"
                        + "请确认已安装或启用 Java 8 及以上版本，并正确配置 "
                        + "PATH/JAVA_HOME；若环境正常，请重新获取完整的 "
                        + "sdd2-control.jar。详情："
                        + exc.getClass().getSimpleName() + ": "
                        + String.valueOf(exc.getMessage())
                )
            ));
            return 3;
        }
    }

    public static void main(String[] argv) {
        System.exit(runMain(argv));
    }
}
